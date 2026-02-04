from fastapi import APIRouter, Depends, HTTPException, Request
from datetime import datetime
import time
from ..models.schemas import (
    DetectScamRequest, DetectScamResponse, EngagementMetrics,
    ExtractedIntelligence, CallbackPayload
)
from ..models.firebase_models import (
    FirestoreScamIntelligence,
    FirestoreExtractedData,
    FirestoreAPILog
)
from ..api.auth import validate_api_key
from ..core.detector import ScamDetector
from ..core.agent import AIAgent
from ..core.extractor import IntelligenceExtractor
from ..utils.session_manager import session_manager
from ..utils.callback import send_evaluation_callback, should_trigger_callback
from ..repositories.firestore_repository import firestore_repo

router = APIRouter()


@router.post("/api/detect-scam", response_model=DetectScamResponse)
async def detect_scam(
    request: DetectScamRequest,
    fastapi_req: Request,
    api_key: str = Depends(validate_api_key)
):
    """
    Main scam detection and engagement endpoint
    """
    start_time = time.time()
    session_id = request.sessionId
    
    try:
        # Get current message
        current_message = request.message
        language = request.metadata.language
        
        # NOTE: Session logging happens inside update_session_metrics
        # Update session with new message
        message_dict = {
            'sender': current_message.sender,
            'text': current_message.text,
            'timestamp': current_message.timestamp
        }
        
        session_data = session_manager.update_session_metrics(session_id, message_dict)
        
        # Get full conversation history
        full_history = session_data.get('conversation_history', [])
        
        # Detect scam
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
                    
                    # Log agent response to history & Firestore
                    agent_msg = {
                        'sender': 'agent',
                        'text': agent_response,
                        'timestamp': datetime.now().isoformat()
                    }
                    session_manager.update_session_metrics(session_id, agent_msg)
                    
                except Exception as e:
                    print(f"Error generating agent response: {e}")
                    agent_response = "Could you please provide more details?"
        
        # Extract intelligence
        extracted_intel = IntelligenceExtractor.extract_from_conversation(
            full_history,
            language
        )
        
        # Merge with existing intelligence
        merged_intel = session_manager.merge_intelligence(
            session_id,
            extracted_intel.model_dump()
        )
        
        # LOG SCAM INTELLIGENCE TO FIRESTORE
        if scam_detected:
            try:
                intel_data = FirestoreExtractedData(**merged_intel)
                
                # Generate agent notes for logging
                if not agent_notes:
                    agent_notes = AIAgent.generate_agent_notes(full_history, merged_intel)

                scam_intel = FirestoreScamIntelligence(
                    sessionId=session_id,
                    scamType=detection_result.get('scam_type', 'Unknown'),
                    confidence=detection_result.get('confidence', 0.0),
                    language=language,
                    extractedData=intel_data,
                    callbackSent=False, # Will update if callback sent
                    agentNotes=agent_notes
                )
                firestore_repo.save_scam_intelligence(scam_intel)
            except Exception as e:
                print(f"Error logging scam intelligence: {e}")
        
        # Generate agent notes (if not already done)
        if not agent_notes:
            agent_notes = AIAgent.generate_agent_notes(full_history, merged_intel)
        
        # Metrics
        total_messages = len(full_history)
        engagement_duration = total_messages * 30
        
        engagement_metrics = EngagementMetrics(
            engagementDurationSeconds=engagement_duration,
            totalMessagesExchanged=total_messages
        )
        
        # Prepare extracted intelligence response
        intel_response = ExtractedIntelligence(**merged_intel)
        
        # Check callback
        callback_triggered = False
        if scam_detected and should_trigger_callback(session_data):
            callback_payload = CallbackPayload(
                sessionId=session_id,
                scamDetected=scam_detected,
                totalMessagesExchanged=total_messages,
                extractedIntelligence=intel_response,
                agentNotes=agent_notes
            )
            
            import asyncio
            asyncio.create_task(send_evaluation_callback(callback_payload))
            callback_triggered = True
        
        # Log API Request
        duration = (time.time() - start_time) * 1000
        api_log = FirestoreAPILog(
            endpoint="/api/detect-scam",
            method="POST",
            statusCode=200,
            responseTime=duration,
            sessionId=session_id
        )
        firestore_repo.log_api_request(api_log)
        
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
        # Log Error
        duration = (time.time() - start_time) * 1000
        api_log = FirestoreAPILog(
            endpoint="/api/detect-scam",
            method="POST",
            statusCode=500,
            responseTime=duration,
            sessionId=session_id,
            errorMessage=str(e)
        )
        firestore_repo.log_api_request(api_log)
        
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
