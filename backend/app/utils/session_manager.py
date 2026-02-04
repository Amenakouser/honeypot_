import json
import redis
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
from datetime import datetime

from ..repositories.firestore_repository import firestore_repo
from ..models.firebase_models import (
    FirestoreSession,
    FirestoreSessionMetadata,
    FirestoreConversationMessage,
    MessageRole,
    SessionStatus
)

load_dotenv()


class SessionManager:
    """
    Manage conversation sessions using Redis for caching and Firestore for persistence.
    
    Strategy:
    - Redis: Active session state, fast retrieval
    - Firestore: Persistent logs, analytics, historical data
    """
    
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()
            self.use_redis = True
        except Exception as e:
            print(f"Redis connection failed: {e}. Using in-memory storage.")
            self.use_redis = False
            self.memory_store = {}
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data by ID (prefer Redis)"""
        try:
            if self.use_redis:
                data = self.redis_client.get(f"session:{session_id}")
                return json.loads(data) if data else None
            else:
                return self.memory_store.get(session_id)
        except Exception as e:
            print(f"Error getting session: {e}")
            return None
    
    def save_session(self, session_id: str, data: Dict, expire_seconds: int = 3600):
        """Save session data to Redis/Memory"""
        try:
            if self.use_redis:
                self.redis_client.setex(
                    f"session:{session_id}",
                    expire_seconds,
                    json.dumps(data)
                )
            else:
                self.memory_store[session_id] = data
        except Exception as e:
            print(f"Error saving session: {e}")
    
    def update_session_metrics(self, session_id: str, new_message: Dict):
        """
        Update session metrics and log to Firestore.
        
        Args:
            session_id: Session ID
            new_message: Message dictionary {sender, text, timestamp}
        """
        session = self.get_session(session_id)
        is_new_session = session is None
        
        if is_new_session:
            session = {
                'conversation_history': [],
                'total_messages': 0,
                'start_time': new_message.get('timestamp'),
                'extracted_intel': {
                    'bankAccounts': [],
                    'upids': [],
                    'phishingLinks': [],
                    'phoneNumbers': [],
                    'suspiciousKeywords': []
                },
                'metadata': {
                    'channel': 'SMS',  # Default, should come from request
                    'language': 'English'
                }
            }
        
        # Add message to history
        session['conversation_history'].append(new_message)
        session['total_messages'] = len(session['conversation_history'])
        
        # Save to Redis
        self.save_session(session_id, session)
        
        # LOGGING TO FIRESTORE
        try:
            # 1. Create/Update Session Document
            if is_new_session:
                metadata = FirestoreSessionMetadata(
                    channel=session.get('metadata', {}).get('channel', 'SMS'),
                    language=session.get('metadata', {}).get('language', 'English')
                )
                
                firestore_session = FirestoreSession(
                    sessionId=session_id,
                    createdAt=datetime.now(),
                    metadata=metadata,
                    totalMessages=1
                )
                firestore_repo.create_session(firestore_session)
            else:
                # Update session metrics
                firestore_repo.update_session(session_id, {
                    "totalMessages": session['total_messages'],
                    "updatedAt": datetime.now()
                })
            
            # 2. Add Message to Subcollection
            role = MessageRole.SCAMMER if new_message.get('sender') == 'scammer' else MessageRole.AGENT
            
            # Parse timestamp if string
            ts = new_message.get('timestamp')
            if isinstance(ts, str):
                try:
                    ts = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                except:
                    ts = datetime.now()
            
            msg = FirestoreConversationMessage(
                role=role,
                content=new_message.get('text', ''),
                timestamp=ts or datetime.now()
            )
            
            firestore_repo.add_conversation_message(session_id, msg)
            
        except Exception as e:
            print(f"Error logging to Firestore: {e}")
            
        return session
    
    def merge_intelligence(self, session_id: str, new_intel: Dict):
        """Merge new intelligence data with existing and update Firestore"""
        session = self.get_session(session_id) or {'extracted_intel': {}}
        
        existing_intel = session.get('extracted_intel', {})
        
        # Merge lists and remove duplicates
        for key in ['bankAccounts', 'upids', 'phishingLinks', 'phoneNumbers', 'suspiciousKeywords']:
            existing = set(existing_intel.get(key, []))
            new = set(new_intel.get(key, []))
            existing_intel[key] = list(existing.union(new))
        
        session['extracted_intel'] = existing_intel
        self.save_session(session_id, session)
        
        return existing_intel
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session"""
        session = self.get_session(session_id)
        return session.get('conversation_history', []) if session else []
    
    def delete_session(self, session_id: str):
        """Delete from Redis and mark as completed in Firestore"""
        try:
            # Mark in Firestore
            firestore_repo.update_session_status(session_id, SessionStatus.COMPLETED)
            
            # Delete from Redis
            if self.use_redis:
                self.redis_client.delete(f"session:{session_id}")
            else:
                self.memory_store.pop(session_id, None)
        except Exception as e:
            print(f"Error deleting session: {e}")


# Global instance
session_manager = SessionManager()
