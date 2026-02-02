import React, { useState, useEffect } from 'react';
import ChatWindow from '../components/ChatWindow';
import IntelPanel from '../components/IntelPanel';
import Controls from '../components/Controls';
import { detectScam } from '../services/api';

const Dashboard = () => {
    const [sessionId, setSessionId] = useState(`session-${Date.now()}`);
    const [messages, setMessages] = useState([]);
    const [language, setLanguage] = useState('English');
    const [channel, setChannel] = useState('SMS');
    const [autoMode, setAutoMode] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    // Detection metrics
    const [scamProbability, setScamProbability] = useState(0);
    const [keywords, setKeywords] = useState([]);
    const [agentActive, setAgentActive] = useState(false);

    // Extracted intelligence
    const [extractedIntel, setExtractedIntel] = useState({
        upids: [],
        bankAccounts: [],
        phoneNumbers: [],
        phishingLinks: [],
        suspiciousKeywords: []
    });

    // API logs
    const [apiLogs, setApiLogs] = useState([]);
    const [showLogs, setShowLogs] = useState(false);

    const sendMessage = async (text, sender = 'scammer') => {
        const newMessage = {
            sender,
            text,
            timestamp: new Date().toISOString()
        };

        // Add message to UI immediately
        setMessages(prev => [...prev, newMessage]);
        setIsLoading(true);

        try {
            // Call API
            const conversationHistory = messages.map(msg => ({
                sender: msg.sender,
                text: msg.text,
                timestamp: msg.timestamp
            }));

            const requestData = {
                sessionId,
                message: newMessage,
                conversationHistory,
                metadata: {
                    channel,
                    language,
                    locale: 'IN'
                }
            };

            const response = await detectScam(
                sessionId,
                newMessage,
                conversationHistory,
                { channel, language, locale: 'IN' }
            );

            // Log API call
            setApiLogs(prev => [...prev, {
                timestamp: new Date().toISOString(),
                request: requestData,
                response
            }]);

            // Update metrics
            if (sender === 'scammer') {
                // Estimate probability from keywords and intel
                const hasIntel = response.extractedIntelligence.upids.length > 0 ||
                    response.extractedIntelligence.bankAccounts.length > 0 ||
                    response.extractedIntelligence.phoneNumbers.length > 0 ||
                    response.extractedIntelligence.phishingLinks.length > 0;

                const estimatedProb = response.scamDetected ?
                    (hasIntel ? 0.9 : 0.7) :
                    (response.extractedIntelligence.suspiciousKeywords.length > 0 ? 0.4 : 0.1);

                setScamProbability(estimatedProb);
                setKeywords(response.extractedIntelligence.suspiciousKeywords);
                setAgentActive(response.scamDetected);
            }

            // Update extracted intelligence
            setExtractedIntel(response.extractedIntelligence);

            // If agent responded, add its message
            if (response.agentResponse && autoMode) {
                setTimeout(() => {
                    const agentMessage = {
                        sender: 'user',
                        text: response.agentResponse,
                        timestamp: new Date().toISOString()
                    };
                    setMessages(prev => [...prev, agentMessage]);
                }, 1000);
            } else if (response.agentResponse) {
                // Show agent response even if auto-mode is off
                const agentMessage = {
                    sender: 'user',
                    text: response.agentResponse,
                    timestamp: new Date().toISOString()
                };
                setMessages(prev => [...prev, agentMessage]);
            }

        } catch (error) {
            console.error('Error sending message:', error);
            alert('Error communicating with API. Please check your backend is running.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleLoadScenario = (scenario) => {
        // Reset session
        startNew();

        // Load scenario messages
        setLanguage(scenario.language);
        setChannel(scenario.channel);

        setTimeout(() => {
            scenario.messages.forEach((msg, idx) => {
                setTimeout(() => {
                    sendMessage(msg.text, msg.sender);
                }, idx * 1500);
            });
        }, 500);
    };

    const startNew = () => {
        setSessionId(`session-${Date.now()}`);
        setMessages([]);
        setScamProbability(0);
        setKeywords([]);
        setAgentActive(false);
        setExtractedIntel({
            upids: [],
            bankAccounts: [],
            phoneNumbers: [],
            phishingLinks: [],
            suspiciousKeywords: []
        });
        setApiLogs([]);
    };

    const handleExport = () => {
        const exportData = {
            sessionId,
            messages,
            metrics: {
                scamProbability,
                keywords,
                totalMessages: messages.length
            },
            extractedIntel,
            apiLogs
        };

        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `honeypot-session-${sessionId}.json`;
        a.click();
    };

    return (
        <div className="min-h-screen p-6">
            {/* Header */}
            <div className="text-center mb-6">
                <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">🍯 AI Honeypot Scam Detection System</h1>
                <p className="text-gray-600 mt-2">
                    Intelligent scam detection and engagement platform
                </p>
            </div>

            {/* Main Content */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                {/* Left: Chat Window */}
                <div className="lg:col-span-2">
                    <ChatWindow
                        messages={messages}
                        onSendMessage={sendMessage}
                        language={language}
                        setLanguage={setLanguage}
                        channel={channel}
                        setChannel={setChannel}
                        autoMode={autoMode}
                        setAutoMode={setAutoMode}
                        isLoading={isLoading}
                    />
                </div>

                {/* Right: Intelligence Panel */}
                <div className="lg:col-span-1">
                    <IntelPanel
                        scamProbability={scamProbability}
                        keywords={keywords}
                        agentActive={agentActive}
                        totalMessages={messages.length}
                        extractedIntel={extractedIntel}
                    />
                </div>
            </div>

            {/* Bottom: Controls */}
            <div className="w-full">
                <Controls
                    onLoadScenario={handleLoadScenario}
                    onStartNew={startNew}
                    onExport={handleExport}
                    sessionData={{ sessionId, messages, extractedIntel }}
                    apiLogs={apiLogs}
                    showLogs={showLogs}
                    setShowLogs={setShowLogs}
                />
            </div>
        </div>
    );
};

export default Dashboard;
