import React from 'react';

const IntelPanel = ({
    scamProbability,
    keywords,
    agentActive,
    totalMessages,
    extractedIntel
}) => {
    const probabilityColor = scamProbability >= 0.7 ? 'text-red-600' :
        scamProbability >= 0.5 ? 'text-orange-600' :
            'text-green-600';

    return (
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-5 space-y-4 h-[600px] overflow-y-auto">
            {/* Detection Metrics */}
            <div className="border-b border-gray-200 pb-4 last:border-b-0">
                <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">Detection Metrics</h3>
                <div className="flex justify-between items-start py-2 border-b border-gray-100 last:border-b-0">
                    <span className="text-sm text-gray-600 font-medium">Scam Probability:</span>
                    <span className={`text-sm text-gray-900 font-bold ${probabilityColor}`}>
                        {(scamProbability * 100).toFixed(0)}%
                    </span>
                </div>
                <div className="flex justify-between items-start py-2 border-b border-gray-100 last:border-b-0">
                    <span className="text-sm text-gray-600 font-medium">Keywords:</span>
                    <div className="flex flex-wrap gap-1 mt-1">
                        {keywords.length > 0 ? (
                            keywords.slice(0, 5).map((kw, idx) => (
                                <span key={idx} className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs font-medium">
                                    {kw}
                                </span>
                            ))
                        ) : (
                            <span className="text-gray-400 text-sm">None detected</span>
                        )}
                    </div>
                </div>
                <div className="flex justify-between items-start py-2 border-b border-gray-100 last:border-b-0">
                    <span className="text-sm text-gray-600 font-medium">Agent Active:</span>
                    <span className="text-sm text-gray-900">
                        {agentActive ? '✅ Yes' : '⏸️ No'}
                    </span>
                </div>
                <div className="flex justify-between items-start py-2 border-b border-gray-100 last:border-b-0">
                    <span className="text-sm text-gray-600 font-medium">Messages:</span>
                    <span className="text-sm text-gray-900">{totalMessages}</span>
                </div>
            </div>

            {/* Extracted Intelligence */}
            <div className="border-b border-gray-200 pb-4 last:border-b-0">
                <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">Extracted Intelligence</h3>

                {extractedIntel.upids.length > 0 && (
                    <div className="mb-3">
                        <span className="block text-sm font-semibold text-gray-700 mb-1">💳 UPI IDs:</span>
                        <div className="flex flex-wrap gap-2">
                            {extractedIntel.upids.map((upi, idx) => (
                                <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-mono">{upi}</span>
                            ))}
                        </div>
                    </div>
                )}

                {extractedIntel.bankAccounts.length > 0 && (
                    <div className="mb-3">
                        <span className="block text-sm font-semibold text-gray-700 mb-1">🏦 Bank Accounts:</span>
                        <div className="flex flex-wrap gap-2">
                            {extractedIntel.bankAccounts.map((acc, idx) => (
                                <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-mono">{acc}</span>
                            ))}
                        </div>
                    </div>
                )}

                {extractedIntel.phoneNumbers.length > 0 && (
                    <div className="mb-3">
                        <span className="block text-sm font-semibold text-gray-700 mb-1">📱 Phone Numbers:</span>
                        <div className="flex flex-wrap gap-2">
                            {extractedIntel.phoneNumbers.map((phone, idx) => (
                                <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-mono">{phone}</span>
                            ))}
                        </div>
                    </div>
                )}

                {extractedIntel.phishingLinks.length > 0 && (
                    <div className="mb-3">
                        <span className="block text-sm font-semibold text-gray-700 mb-1">🔗 Links:</span>
                        <div className="flex flex-wrap gap-2">
                            {extractedIntel.phishingLinks.map((link, idx) => (
                                <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-mono text-xs break-all">
                                    {link.substring(0, 40)}...
                                </span>
                            ))}
                        </div>
                    </div>
                )}

                {extractedIntel.upids.length === 0 &&
                    extractedIntel.bankAccounts.length === 0 &&
                    extractedIntel.phoneNumbers.length === 0 &&
                    extractedIntel.phishingLinks.length === 0 && (
                        <p className="text-gray-400 text-sm">No intelligence extracted yet</p>
                    )}
            </div>
        </div>
    );
};

export default IntelPanel;
