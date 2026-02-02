from typing import List, Dict
import re


class ScamDetector:
    """Scam detection engine using rule-based and pattern matching"""
    
    # Urgency indicators (multilingual)
    URGENCY_PATTERNS = {
        'English': [
            r'urgently?', r'immediately?', r'right\s+now', r'act\s+now',
            r'limited\s+time', r'expires?\s+(soon|today|tonight)',
            r'within\s+\d+\s+(hours?|minutes?)', r'before\s+\d+'
        ],
        'Hindi': [
            r'तुरंत', r'जल्दी', r'अभी', r'समय\s+सीमित'
        ],
        'Tamil': [
            r'உடனடி', r'விரைவாக', r'இப்போதே'
        ],
        'Telugu': [
            r'తక్షణం', r'వెంటనే', r'ఇప్పుడే'
        ],
        'Malayalam': [
            r'ഉടൻ', r'വേഗം', r'ഇപ്പോൾ'
        ]
    }
    
    # Impersonation patterns
    IMPERSONATION_PATTERNS = [
        r'\b(bank|HDFC|ICICI|SBI|Axis|Kotak|PNB)\b',
        r'\b(PayTM|PhonePe|GPay|Google\s+Pay|WhatsApp)\b',
        r'\b(government|ministry|RBI|income\s+tax|GST)\b',
        r'\b(police|cyber\s+cell|law\s+enforcement)\b',
        r'\b(Amazon|Flipkart|courier|delivery)\b',
        r'\bसरकार\b', r'\bपुलिस\b', r'\bबैंक\b'
    ]
    
    # Financial request patterns
    FINANCIAL_PATTERNS = [
        r'\b(account|खाता)\s+(number|नंबर|details|blocked|बंद|suspended)',
        r'\b(CVV|सीवीवी|OTP|ओटीपी|PIN|पिन)\b',
        r'\b(card|कार्ड)\s+(number|नंबर|details|expired)',
        r'\b(UPI|यूपीआई)\s+(ID|pin|password)',
        r'\b(verify|सत्यापित|confirm|पुष्टि)\s+(KYC|केवाईसी|details|account)',
        r'\b(refund|रिफंड|cashback|reward|इनाम|prize)\b'
    ]
    
    # Phishing indicators
    PHISHING_PATTERNS = [
        r'click\s+(here|link|below)',
        r'download\s+app',
        r'install\s+(now|application)',
        r'update\s+(details|information|account)',
        r'bit\.ly|tinyurl|goo\.gl',  # URL shorteners
        r'यहां\s+क्लिक', r'लिंक\s+पर'
    ]
    
    # Prize/lottery scam patterns
    PRIZE_PATTERNS = [
        r'\b(won|जीत|winner|विजेता|congratulations|बधाई)\b',
        r'\b(prize|इनाम|lottery|लॉटरी|reward|पुरस्कार)\b',
        r'\b(claim|दावा)\s+(now|अभी|today)',
        r'₹\s*\d+\s*(lakh|lakhs|crore|crores|thousand)'
    ]
    
    @classmethod
    def detect(cls, text: str, language: str = 'English', conversation_history: List[Dict] = None) -> Dict:
        """
        Detect if text is a scam
        Returns: {
            'is_scam': bool,
            'confidence': float (0-1),
            'reasons': List[str],
            'keywords': List[str]
        }
        """
        text_lower = text.lower()
        reasons = []
        keywords = []
        score = 0.0
        
        # Check urgency
        urgency_count = 0
        for lang, patterns in cls.URGENCY_PATTERNS.items():
            if lang == language or lang == 'English':
                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    if matches:
                        urgency_count += len(matches)
                        keywords.extend(matches)
        
        if urgency_count > 0:
            score += min(0.2, urgency_count * 0.1)
            reasons.append("Urgency tactics detected")
        
        # Check impersonation
        impersonation_matches = []
        for pattern in cls.IMPERSONATION_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                impersonation_matches.extend(matches)
        
        if impersonation_matches:
            score += 0.25
            reasons.append("Impersonation of trusted entity")
            keywords.extend(impersonation_matches)
        
        # Check financial requests
        financial_matches = []
        for pattern in cls.FINANCIAL_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                financial_matches.extend(matches)
        
        if financial_matches:
            score += 0.3
            reasons.append("Requesting sensitive financial information")
            keywords.extend(financial_matches)
        
        # Check phishing indicators
        phishing_matches = []
        for pattern in cls.PHISHING_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                phishing_matches.extend(matches)
        
        if phishing_matches:
            score += 0.2
            reasons.append("Phishing attempt detected")
            keywords.extend(phishing_matches)
        
        # Check prize/lottery scams
        prize_matches = []
        for pattern in cls.PRIZE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                prize_matches.extend(matches)
        
        if prize_matches:
            score += 0.25
            reasons.append("Prize/lottery scam indicators")
            keywords.extend(prize_matches)
        
        # URL detection (any URL in first message is suspicious)
        if re.search(r'https?://', text):
            score += 0.15
            reasons.append("Contains URL link")
        
        # Bonus score if multiple indicators
        if len(reasons) >= 3:
            score += 0.1
        
        # Cap confidence at 1.0
        confidence = min(1.0, score)
        
        # Consider it a scam if confidence > 0.5
        is_scam = confidence >= 0.5
        
        return {
            'is_scam': is_scam,
            'confidence': confidence,
            'reasons': reasons,
            'keywords': list(set(keywords))
        }
