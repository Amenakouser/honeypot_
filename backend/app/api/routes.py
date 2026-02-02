from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from ..models.schemas import (
    DetectScamRequest, DetectScamResponse, EngagementMetrics,
    ExtractedIntelligence, CallbackPayload
)
from ..api.auth import validate_api_key
from ..core.detector import ScamDetector
from ..core.agent import AIAgent
from ..core.extractor import IntelligenceExtractor
from ..utils.session_manager import session_manager
from ..utils.callback import send_evaluation_callback, should_trigger_callback

router = APIRouter()


@router.post("/api/detect-scam", response_model=DetectScamResponse)
async def detect_scam(
    request: DetectScamRequest,
    api_key: str = Depends(validate_api_key)
):
    """
    Main scam detection and engagement endpoint
    
    Process:
    1. Detect if message is a scam
    2. If scam detected, engage with AI agent
    3. Extract intelligence from conversation
    4. Update session metrics
    5. Trigger callback if criteria met
    """
    
    try:
        # Get current message
        current_message = request.message
        session_id = request.sessionId
        language = request.metadata.language
        
        # Update session with new message
        message_dict = {
            'sender': current_message.sender,
            'text': current_message.text,
            'timestamp': current_message.timestamp
        }
        
        session_data = session_manager.update_session_metrics(session_id, message_dict)
        
        # Get full conversation history
        full_history = session_data.get('conversation_history', [])
        
        # Detect scam (only if message is from scammer)
        scam_detected = False
        agent_response = None
        agent_notes = ""
        
        if current_message.sender == "scammer":
            # Run scam detection
            detection_result = ScamDetector.detect(
                current_message.text,
                language,
                full_history
            )
            
            scam_detected = detection_result['is_scam']
            
            # If scam detected, generate agent response
            if scam_detected:
                try:
                    agent_response = AIAgent.generate_response(
                        current_message.text,
                        full_history,
                        language
                    )
                except Exception as e:
                    print(f"Error generating agent response: {e}")
                    agent_response = "Could you please provide more details?"
        
        # Extract intelligence from entire conversation
        extracted_intel = IntelligenceExtractor.extract_from_conversation(
            full_history,
            language
        )
        
        # Merge with existing intelligence
        merged_intel = session_manager.merge_intelligence(
            session_id,
            extracted_intel.model_dump()
        )
        
        # Generate agent notes
        agent_notes = AIAgent.generate_agent_notes(
            full_history,
            merged_intel
        )
        
        # Calculate engagement metrics
        total_messages = len(full_history)
        
        # Calculate duration (simplified - using message count as proxy)
        engagement_duration = total_messages * 30  # Assume ~30 seconds per exchange
        
        engagement_metrics = EngagementMetrics(
            engagementDurationSeconds=engagement_duration,
            totalMessagesExchanged=total_messages
        )
        
        # Prepare extracted intelligence response
        intel_response = ExtractedIntelligence(**merged_intel)
        
        # Check if we should trigger callback
        if scam_detected and should_trigger_callback(session_data):
            callback_payload = CallbackPayload(
                sessionId=session_id,
                scamDetected=scam_detected,
                totalMessagesExchanged=total_messages,
                extractedIntelligence=intel_response,
                agentNotes=agent_notes
            )
            
            # Send callback (don't wait for it)
            import asyncio
            asyncio.create_task(send_evaluation_callback(callback_payload))
        
        # Build response
        response = DetectScamResponse(
            status="success",
            scamDetected=scam_detected,
            engagementMetrics=engagement_metrics,
            extractedIntelligence=intel_response,
            agentNotes=agent_notes,
            agentResponse=agent_response if scam_detected else None
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "honeypot-api"}


@router.post("/api/reset-session/{session_id}")
async def reset_session(session_id: str, api_key: str = Depends(validate_api_key)):
    """Reset/delete a session"""
    session_manager.delete_session(session_id)
    return {"status": "success", "message": f"Session {session_id} reset"}


@router.get("/api/session/{session_id}")
async def get_session(session_id: str, api_key: str = Depends(validate_api_key)):
    """Get session data"""
    session_data = session_manager.get_session(session_id)
    
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"status": "success", "data": session_data}
