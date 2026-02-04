"""
Firestore repository for database operations.

This module provides a clean interface for all Firestore operations,
including CRUD operations for sessions, conversations, scam intelligence,
and API logs.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
from google.cloud import firestore

from ..core.firebase import get_firestore_client
from ..models.firebase_models import (
    FirestoreSession,
    FirestoreConversationMessage,
    FirestoreScamIntelligence,
    FirestoreAPILog,
    SessionStatus,
    MessageRole,
)

logger = logging.getLogger(__name__)


class FirestoreRepository:
    """Repository for Firestore database operations"""
    
    def __init__(self):
        self.db = get_firestore_client()
        self.enabled = self.db is not None
        
        if not self.enabled:
            logger.warning("Firestore is not initialized - operations will be skipped")
    
    # ==================== Session Operations ====================
    
    def create_session(self, session: FirestoreSession) -> bool:
        """
        Create a new session document.
        
        Args:
            session: FirestoreSession model
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            doc_ref = self.db.collection("sessions").document(session.sessionId)
            doc_ref.set(session.to_dict())
            logger.info(f"Created session: {session.sessionId}")
            return True
        except Exception as e:
            logger.error(f"Failed to create session {session.sessionId}: {str(e)}")
            return False
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a session document by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data or None
        """
        if not self.enabled:
            return None
        
        try:
            doc_ref = self.db.collection("sessions").document(session_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"Failed to get session {session_id}: {str(e)}")
            return None
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a session document.
        
        Args:
            session_id: Session ID
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            doc_ref = self.db.collection("sessions").document(session_id)
            updates["updatedAt"] = datetime.utcnow()
            doc_ref.update(updates)
            logger.info(f"Updated session: {session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to update session {session_id}: {str(e)}")
            return False
    
    def update_session_status(self, session_id: str, status: SessionStatus) -> bool:
        """
        Update session status.
        
        Args:
            session_id: Session ID
            status: New status
            
        Returns:
            True if successful, False otherwise
        """
        return self.update_session(session_id, {"status": status.value})
    
    # ==================== Conversation Operations ====================
    
    def add_conversation_message(
        self,
        session_id: str,
        message: FirestoreConversationMessage
    ) -> bool:
        """
        Add a message to a session's conversation subcollection.
        
        Args:
            session_id: Session ID
            message: Conversation message
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            # Add message to conversations subcollection
            conversations_ref = (
                self.db.collection("sessions")
                .document(session_id)
                .collection("conversations")
            )
            conversations_ref.add(message.to_dict())
            
            # Update session message count
            self.db.collection("sessions").document(session_id).update({
                "totalMessages": firestore.Increment(1),
                "updatedAt": datetime.utcnow()
            })
            
            logger.info(f"Added message to session {session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add message to session {session_id}: {str(e)}")
            return False
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get all messages from a session's conversation.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of conversation messages
        """
        if not self.enabled:
            return []
        
        try:
            conversations_ref = (
                self.db.collection("sessions")
                .document(session_id)
                .collection("conversations")
                .order_by("timestamp")
            )
            
            messages = []
            for doc in conversations_ref.stream():
                messages.append(doc.to_dict())
            
            return messages
        except Exception as e:
            logger.error(f"Failed to get conversation history for {session_id}: {str(e)}")
            return []
    
    # ==================== Scam Intelligence Operations ====================
    
    def save_scam_intelligence(self, intelligence: FirestoreScamIntelligence) -> bool:
        """
        Save scam intelligence data.
        
        Args:
            intelligence: Scam intelligence model
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            self.db.collection("scam_intelligence").add(intelligence.to_dict())
            
            # Mark session as scam detected
            self.update_session(intelligence.sessionId, {"scamDetected": True})
            
            logger.info(f"Saved scam intelligence for session {intelligence.sessionId}")
            return True
        except Exception as e:
            logger.error(f"Failed to save scam intelligence: {str(e)}")
            return False
    
    def get_scam_intelligence_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get all scam intelligence for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of scam intelligence documents
        """
        if not self.enabled:
            return []
        
        try:
            query = (
                self.db.collection("scam_intelligence")
                .where("sessionId", "==", session_id)
                .order_by("flaggedAt", direction=firestore.Query.DESCENDING)
            )
            
            results = []
            for doc in query.stream():
                results.append(doc.to_dict())
            
            return results
        except Exception as e:
            logger.error(f"Failed to get scam intelligence for {session_id}: {str(e)}")
            return []
    
    # ==================== API Log Operations ====================
    
    def log_api_request(self, log: FirestoreAPILog) -> bool:
        """
        Log an API request.
        
        Args:
            log: API log model
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            self.db.collection("api_logs").add(log.to_dict())
            return True
        except Exception as e:
            logger.error(f"Failed to log API request: {str(e)}")
            return False
    
    # ==================== Analytics Operations ====================
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent sessions.
        
        Args:
            limit: Maximum number of sessions to return
            
        Returns:
            List of session documents
        """
        if not self.enabled:
            return []
        
        try:
            query = (
                self.db.collection("sessions")
                .order_by("createdAt", direction=firestore.Query.DESCENDING)
                .limit(limit)
            )
            
            results = []
            for doc in query.stream():
                results.append(doc.to_dict())
            
            return results
        except Exception as e:
            logger.error(f"Failed to get recent sessions: {str(e)}")
            return []
    
    def get_scam_statistics(self) -> Dict[str, Any]:
        """
        Get scam detection statistics.
        
        Returns:
            Dictionary with statistics
        """
        if not self.enabled:
            return {}
        
        try:
            # Count total scams
            scam_query = self.db.collection("scam_intelligence")
            total_scams = len(list(scam_query.stream()))
            
            # Count sessions with scams
            session_query = self.db.collection("sessions").where("scamDetected", "==", True)
            scam_sessions = len(list(session_query.stream()))
            
            return {
                "totalScamsDetected": total_scams,
                "sessionsWithScams": scam_sessions,
            }
        except Exception as e:
            logger.error(f"Failed to get scam statistics: {str(e)}")
            return {}


# Singleton instance
firestore_repo = FirestoreRepository()
