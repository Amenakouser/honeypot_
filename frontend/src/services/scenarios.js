export const SAMPLE_SCENARIOS = {
    'Bank Fraud': {
        messages: [
            {
                sender: 'scammer',
                text: 'URGENT: Your SBI account will be blocked in 2 hours. Click here to verify: http://bit.ly/verify-sbi-urgent. Enter your account number and CVV immediately.',
                timestamp: new Date().toISOString()
            }
        ],
        language: 'English',
        channel: 'SMS'
    },
    'UPI Fraud': {
        messages: [
            {
                sender: 'scammer',
                text: 'Your PhonePe payment of ₹5000 has failed. To receive refund, kindly share your UPI ID and verify OTP we will send.',
                timestamp: new Date().toISOString()
            }
        ],
        language: 'English',
        channel: 'WhatsApp'
    },
    'Phishing': {
        messages: [
            {
                sender: 'scammer',
                text: 'Congratulations! You have won ₹10 lakhs in Amazon lucky draw. Click to claim your prize now: http://tiny.cc/amazon-winner. Limited time offer!',
                timestamp: new Date().toISOString()
            }
        ],
        language: 'English',
        channel: 'Email'
    },
    'Tech Support': {
        messages: [
            {
                sender: 'scammer',
                text: 'Microsoft Security Alert: Your computer has been infected with dangerous virus. Call +91-9876543210 immediately or pay ₹2999 for urgent cleanup. Download our tool: http://fix-virus.now',
                timestamp: new Date().toISOString()
            }
        ],
        language: 'English',
        channel: 'Email'
    },
    'Romance Scam': {
        messages: [
            {
                sender: 'scammer',
                text: 'Hi dear, I am stuck in Mumbai with medical emergency. I need ₹50000 urgently for hospital bills. Please send money to this account: 123456789012. I will return soon.',
                timestamp: new Date().toISOString()
            }
        ],
        language: 'English',
        channel: 'Chat'
    },
    'Hindi Bank Fraud': {
        messages: [
            {
                sender: 'scammer',
                text: 'तुरंत ध्यान दें! आपका HDFC बैंक खाता 1 घंटे में बंद हो जाएगा। अपना खाता नंबर और OTP यहाँ भेजें: +91-8765432109. KYC अपडेट करें।',
                timestamp: new Date().toISOString()
            }
        ],
        language: 'Hindi',
        channel: 'SMS'
    }
};
