import httpx
import os
from typing import Dict
from dotenv import load_dotenv
from ..models.schemas import CallbackPayload

load_dotenv()

CALLBACK_URL = os.getenv(
    "CALLBACK_URL",
    "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
)


async def send_evaluation_callback(payload: CallbackPayload) -> Dict:
    """
    Send final results to evaluation callback endpoint
    
    Args:
        payload: CallbackPayload with session results
    
    Returns:
        Response from callback endpoint
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                CALLBACK_URL,
                json=payload.model_dump(),
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            
            return {
                "status": "success",
                "callback_response": response.json() if response.text else {},
                "status_code": response.status_code
            }
            
    except httpx.TimeoutException:
        return {
            "status": "error",
            "error": "Callback request timed out"
        }
    except httpx.HTTPError as e:
        return {
            "status": "error",
            "error": f"HTTP error: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }


def should_trigger_callback(session_data: Dict) -> bool:
    """
    Determine if callback should be triggered
    
    Triggers when:
    - Scam detected and engagement has progressed (>= 3 messages)
    - OR significant intelligence extracted
    """
    total_messages = session_data.get('total_messages', 0)
    intel = session_data.get('extracted_intel', {})
    
    # Check if significant intelligence was extracted
    intel_count = sum([
        len(intel.get('bankAccounts', [])),
        len(intel.get('upids', [])),
        len(intel.get('phoneNumbers', [])),
        len(intel.get('phishingLinks', []))
    ])
    
    # Trigger if we have multiple messages or extracted intel
    return total_messages >= 3 or intel_count > 0
