import json
import redis
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class SessionManager:
    """Manage conversation sessions using Redis"""
    
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
        """Get session data by ID"""
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
        """Save session data"""
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
        """Update session metrics with new message"""
        session = self.get_session(session_id) or {
            'conversation_history': [],
            'total_messages': 0,
            'start_time': None,
            'extracted_intel': {
                'bankAccounts': [],
                'upids': [],
                'phishingLinks': [],
                'phoneNumbers': [],
                'suspiciousKeywords': []
            }
        }
        
        # Add message to history
        session['conversation_history'].append(new_message)
        session['total_messages'] = len(session['conversation_history'])
        
        # Set start time if first message
        if not session.get('start_time'):
            session['start_time'] = new_message.get('timestamp')
        
        self.save_session(session_id, session)
        return session
    
    def merge_intelligence(self, session_id: str, new_intel: Dict):
        """Merge new intelligence data with existing"""
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
        """Delete a session"""
        try:
            if self.use_redis:
                self.redis_client.delete(f"session:{session_id}")
            else:
                self.memory_store.pop(session_id, None)
        except Exception as e:
            print(f"Error deleting session: {e}")


# Global instance
session_manager = SessionManager()
