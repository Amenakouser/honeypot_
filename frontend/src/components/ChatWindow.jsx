import React, { useState, useRef, useEffect } from 'react';

const ChatWindow = ({
    messages,
    onSendMessage,
    language,
    setLanguage,
    channel,
    setChannel,
    autoMode,
    setAutoMode,
    isLoading
}) => {
    const [inputText, setInputText] = useState('');
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = () => {
        if (inputText.trim()) {
            onSendMessage(inputText, 'scammer');
            setInputText('');
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden h-[600px] flex flex-col">
            {/* Header */}
            <div className="text-white p-4 bg-gradient-to-r from-indigo-500 to-purple-600">
                <h2 className="text-xl font-bold text-gray-800 text-white">Scam Conversation Simulator</h2>
                <div className="flex gap-3 mt-3">
                    <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white text-sm text-gray-900"
                    >
                        <option value="English">English</option>
                        <option value="Hindi">Hindi</option>
                        <option value="Tamil">Tamil</option>
                        <option value="Telugu">Telugu</option>
                        <option value="Malayalam">Malayalam</option>
                    </select>

                    <select
                        value={channel}
                        onChange={(e) => setChannel(e.target.value)}
                        className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white text-sm text-gray-900"
                    >
                        <option value="SMS">SMS</option>
                        <option value="WhatsApp">WhatsApp</option>
                        <option value="Email">Email</option>
                        <option value="Chat">Chat</option>
                    </select>
                </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
                {messages.length === 0 ? (
                    <div className="flex items-center justify-center h-full">
                        <p className="text-gray-500">No messages yet. Start a conversation or load a test scenario.</p>
                    </div>
                ) : (
                    messages.map((msg, idx) => (
                        <div
                            key={idx}
                            className={`p-3 rounded-lg shadow-sm max-w-[80%] animate-fadeIn ${msg.sender === 'scammer' ? 'bg-red-50 border-l-4 border-red-500 mr-auto' : 'bg-green-50 border-l-4 border-green-500 ml-auto'}`}
                        >
                            <div className="flex justify-between items-center mb-1">
                                <span className="font-semibold text-gray-900">
                                    {msg.sender === 'scammer' ? '🚨 Scammer' : '✅ You (AI Agent)'}
                                </span>
                                <span className="text-xs text-gray-500">
                                    {new Date(msg.timestamp).toLocaleTimeString()}
                                </span>
                            </div>
                            <p className="text-gray-900 text-sm">{msg.text}</p>
                        </div>
                    ))
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="bg-white border-t border-gray-200 p-4">
                <textarea
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type scammer's message..."
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none text-gray-900 placeholder-gray-500"
                    rows="2"
                    disabled={isLoading}
                />
                <div className="flex justify-between items-center mt-2">
                    <label className="flex items-center gap-2 text-sm">
                        <input
                            type="checkbox"
                            checked={autoMode}
                            onChange={(e) => setAutoMode(e.target.checked)}
                            className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                        />
                        <span className="text-gray-900">Auto-respond mode</span>
                    </label>
                    <button
                        onClick={handleSend}
                        disabled={!inputText.trim() || isLoading}
                        className="px-4 py-2 text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none bg-gradient-to-r from-purple-600 to-blue-600"
                    >
                        {isLoading ? 'Processing...' : 'Send'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatWindow;
