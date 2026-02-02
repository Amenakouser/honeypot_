from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class Message(BaseModel):
    """Individual message in a conversation"""
    sender: Literal["scammer", "user"]
    text: str
    timestamp: str


class Metadata(BaseModel):
    """Conversation metadata"""
    channel: Literal["SMS", "WhatsApp", "Email", "Chat"]
    language: Literal["English", "Hindi", "Tamil", "Telugu", "Malayalam"]
    locale: str = "IN"


class ExtractedIntelligence(BaseModel):
    """Extracted intelligence from conversation"""
    bankAccounts: List[str] = Field(default_factory=list)
    upids: List[str] = Field(default_factory=list)
    phishingLinks: List[str] = Field(default_factory=list)
    phoneNumbers: List[str] = Field(default_factory=list)
    suspiciousKeywords: List[str] = Field(default_factory=list)


class EngagementMetrics(BaseModel):
    """Engagement metrics"""
    engagementDurationSeconds: int = 0
    totalMessagesExchanged: int = 0


class DetectScamRequest(BaseModel):
    """Request schema for scam detection"""
    sessionId: str
    message: Message
    conversationHistory: List[Message] = Field(default_factory=list)
    metadata: Metadata


class DetectScamResponse(BaseModel):
    """Response schema for scam detection"""
    status: Literal["success", "error"]
    scamDetected: bool
    engagementMetrics: EngagementMetrics
    extractedIntelligence: ExtractedIntelligence
    agentNotes: str
    agentResponse: Optional[str] = None


class CallbackPayload(BaseModel):
    """Payload for evaluation callback"""
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: ExtractedIntelligence
    agentNotes: str
