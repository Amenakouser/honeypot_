import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class AIAgent:
    """AI conversation agent for engaging with scammers"""
    
    SYSTEM_PROMPT = """You are a helpful Indian citizen being targeted by a scammer.

CRITICAL RULES:
1. DO NOT reveal that you know it's a scam
2. Act naturally curious and slightly hesitant but cooperative
3. Your goal is to extract information while keeping them engaged:
   - Bank account numbers
   - UPI IDs
   - Phone numbers
   - Phishing links
   - Any other identifying information

4. Ask clarifying questions to get more details
5. Show mild concern but willingness to help/comply
6. Use natural Indian English expressions (e.g., "kindly", "please do the needful")
7. Occasionally express slight confusion to prompt them to explain more
8. Never be too quick to comply - show realistic hesitation
9. Ask for "verification" or "proof" to extract more data

Remember: You're pretending to be a regular person who doesn't realize this is a scam. Be believable."""

    @classmethod
    def generate_response(cls, message: str, conversation_history: List[Dict], language: str = "English") -> str:
        """
        Generate AI agent response to engage the scammer
        
        Args:
            message: Latest message from scammer
            conversation_history: Previous conversation messages
            language: Language of conversation
        
        Returns:
            Agent's response text
        """
        
        # Build conversation for OpenAI API
        messages = [{"role": "system", "content": cls.SYSTEM_PROMPT}]
        
        # Add conversation history
        for msg in conversation_history:
            role = "assistant" if msg.get('sender') == 'user' else "user"
            messages.append({
                "role": role,
                "content": msg.get('text', '')
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })
        
        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.8,
                max_tokens=150,
                presence_penalty=0.6,
                frequency_penalty=0.3
            )
            
            agent_response = response.choices[0].message.content.strip()
            
            # Add language-specific touches if not English
            if language == "Hindi":
                agent_response = cls._add_hindi_touches(agent_response)
            
            return agent_response
            
        except Exception as e:
            # Fallback response if API fails
            print(f"Error calling OpenAI API: {e}")
            return cls._get_fallback_response(conversation_history)
    
    @classmethod
    def _add_hindi_touches(cls, text: str) -> str:
        """Add Hindi expressions to English response"""
        # Simple approach - could be enhanced
        replacements = {
            "Please": "Kripya",
            "Thank you": "Dhanyavaad",
            "Okay": "Theek hai",
            "Yes": "Haan"
        }
        
        for eng, hindi in replacements.items():
            if eng in text and len(text.split()) < 20:  # Only for short responses
                text = text.replace(eng, hindi, 1)
                break
        
        return text
    
    @classmethod
    def _get_fallback_response(cls, conversation_history: List[Dict]) -> str:
        """Generate simple fallback response if API fails"""
        
        message_count = len(conversation_history)
        
        fallback_responses = [
            "I'm not sure I understand. Can you explain more?",
            "This seems urgent. What do I need to do exactly?",
            "Can you send me the details? I want to make sure this is legitimate.",
            "How do I verify this is real?",
            "What information do you need from me?",
            "I'm a bit confused. Can you clarify?",
            "Should I call my bank about this?",
            "Is there a customer service number I can verify this with?"
        ]
        
        # Cycle through responses
        return fallback_responses[message_count % len(fallback_responses)]
    
    @classmethod
    def generate_agent_notes(cls, conversation_history: List[Dict], extracted_intel: Dict) -> str:
        """Generate summary notes about the engagement"""
        
        total_messages = len(conversation_history)
        intel_items = sum([
            len(extracted_intel.get('bankAccounts', [])),
            len(extracted_intel.get('upids', [])),
            len(extracted_intel.get('phoneNumbers', [])),
            len(extracted_intel.get('phishingLinks', []))
        ])
        
        notes = f"Engaged scammer for {total_messages} messages. "
        
        if intel_items > 0:
            notes += f"Successfully extracted {intel_items} intelligence items. "
        else:
            notes += "Scammer did not reveal sensitive information yet. "
        
        if extracted_intel.get('suspiciousKeywords'):
            top_keywords = extracted_intel['suspiciousKeywords'][:3]
            notes += f"Key scam indicators: {', '.join(top_keywords)}. "
        
        return notes
