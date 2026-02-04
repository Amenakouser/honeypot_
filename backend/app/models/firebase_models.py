"""
Pydantic models for Firebase Firestore documents.

These models define the structure of documents stored in Firestore
and provide validation and serialization methods.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SessionStatus(str, Enum):
    """Session status enumeration"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class MessageRole(str, Enum):
    """Message role enumeration"""
    SCAMMER = "scammer"
    AGENT = "agent"


class FirestoreSessionMetadata(BaseModel):
    """Metadata for a session document"""
    channel: str = "SMS"
    language: str = "English"
    locale: str = "IN"
    ipAddress: Optional[str] = None
    userAgent: Optional[str] = None


class FirestoreSession(BaseModel):
    """Session document model"""
    sessionId: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    status: SessionStatus = SessionStatus.ACTIVE
    metadata: FirestoreSessionMetadata
    totalMessages: int = 0
    scamDetected: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to Firestore document format"""
        return {
            "sessionId": self.sessionId,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
            "status": self.status.value,
            "metadata": self.metadata.model_dump(),
            "totalMessages": self.totalMessages,
            "scamDetected": self.scamDetected,
        }


class FirestoreConversationMessage(BaseModel):
    """Conversation message document model (subcollection)"""
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to Firestore document format"""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp,
            "metadata": self.metadata or {},
        }


class FirestoreExtractedData(BaseModel):
    """Extracted intelligence data"""
    bankAccounts: List[str] = Field(default_factory=list)
    upiIds: List[str] = Field(default_factory=list)
    phoneNumbers: List[str] = Field(default_factory=list)
    phishingLinks: List[str] = Field(default_factory=list)
    suspiciousKeywords: List[str] = Field(default_factory=list)


class FirestoreScamIntelligence(BaseModel):
    """Scam intelligence document model"""
    sessionId: str
    scamType: str
    confidence: float
    language: str
    extractedData: FirestoreExtractedData
    flaggedAt: datetime = Field(default_factory=datetime.utcnow)
    callbackSent: bool = False
    agentNotes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to Firestore document format"""
        return {
            "sessionId": self.sessionId,
            "scamType": self.scamType,
            "confidence": self.confidence,
            "language": self.language,
            "extractedData": self.extractedData.model_dump(),
            "flaggedAt": self.flaggedAt,
            "callbackSent": self.callbackSent,
            "agentNotes": self.agentNotes,
        }


class FirestoreAPILog(BaseModel):
    """API request log document model"""
    endpoint: str
    method: str
    statusCode: int
    responseTime: float  # milliseconds
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sessionId: Optional[str] = None
    errorMessage: Optional[str] = None
    requestBody: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to Firestore document format"""
        return {
            "endpoint": self.endpoint,
            "method": self.method,
            "statusCode": self.statusCode,
            "responseTime": self.responseTime,
            "timestamp": self.timestamp,
            "sessionId": self.sessionId,
            "errorMessage": self.errorMessage,
            "requestBody": self.requestBody,
        }
