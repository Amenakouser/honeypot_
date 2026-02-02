import re
from typing import List, Dict
from ..models.schemas import ExtractedIntelligence


class IntelligenceExtractor:
    """Extract intelligence information from text"""
    
    # Regex patterns for extraction
    BANK_ACCOUNT_PATTERN = r'\b\d{9,18}\b'
    UPI_PATTERN = r'\b[\w.-]+@(okaxis|okhdfcbank|okicici|oksbi|ybl|axl|paytm|phonepe|gpay|airtel|amazon|freecharge|jiomoney|mobikwik|ola|pockets|whatsapp)\b'
    PHONE_PATTERN = r'(?:\+91|91|0)?[6-9]\d{9}\b'
    URL_PATTERN = r'https?://[^\s]+'
    
    # Suspicious keywords (multilingual)
    SUSPICIOUS_KEYWORDS = {
        'English': [
            'urgent', 'verify', 'account blocked', 'suspended', 'confirm details',
            'click here', 'immediate action', 'prize', 'winner', 'lottery',
            'refund', 'cashback', 'KYC', 'OTP', 'bank details', 'CVV',
            'card number', 'expired', 'update now', 'limited time', 'act now'
        ],
        'Hindi': [
            'तुरंत', 'जल्दी', 'खाता बंद', 'पुष्टि करें', 'अभी करें',
            'इनाम', 'जीत', 'रिफंड', 'केवाईसी', 'ओटीपी', 'बैंक विवरण'
        ],
        'Tamil': [
            'உடனடி', 'சரிபார்', 'கணக்கு முடக்கம்', 'உறுதிப்படுத்து',
            'பரிசு', 'வெற்றி', 'திருப்பி', 'வங்கி விவரங்கள்'
        ],
        'Telugu': [
            'తక్షణం', 'ధృవీకరించు', 'ఖాతా నిలిపివేయబడింది', 'నిర్ధారించండి',
            'బహుమతి', 'విజేత', 'వాపసు', 'బ్యాంక్ వివరాలు'
        ],
        'Malayalam': [
            'ഉടന്', 'സ്ഥിരീകരിക്കുക', 'അക്കൗണ്ട് തടഞ്ഞു', 'സമ്മാനം',
            'വിജയി', 'റിഫണ്ട്', 'ബാങ്ക് വിവരങ്ങൾ'
        ]
    }
    
    @classmethod
    def extract_all(cls, text: str, language: str = 'English') -> ExtractedIntelligence:
        """Extract all intelligence from text"""
        
        # Extract structured data
        bank_accounts = list(set(re.findall(cls.BANK_ACCOUNT_PATTERN, text)))
        upids = list(set(re.findall(cls.UPI_PATTERN, text, re.IGNORECASE)))
        phone_numbers = list(set(re.findall(cls.PHONE_PATTERN, text)))
        phishing_links = list(set(re.findall(cls.URL_PATTERN, text)))
        
        # Extract suspicious keywords
        suspicious_keywords = []
        text_lower = text.lower()
        
        # Check English keywords (always)
        for keyword in cls.SUSPICIOUS_KEYWORDS.get('English', []):
            if keyword.lower() in text_lower:
                suspicious_keywords.append(keyword)
        
        # Check language-specific keywords
        if language in cls.SUSPICIOUS_KEYWORDS:
            for keyword in cls.SUSPICIOUS_KEYWORDS[language]:
                if keyword in text:
                    suspicious_keywords.append(keyword)
        
        suspicious_keywords = list(set(suspicious_keywords))
        
        return ExtractedIntelligence(
            bankAccounts=bank_accounts,
            upids=upids,
            phishingLinks=phishing_links,
            phoneNumbers=phone_numbers,
            suspiciousKeywords=suspicious_keywords
        )
    
    @classmethod
    def extract_from_conversation(cls, messages: List[Dict], language: str = 'English') -> ExtractedIntelligence:
        """Extract intelligence from entire conversation"""
        combined_text = " ".join([msg.get('text', '') for msg in messages])
        return cls.extract_all(combined_text, language)
