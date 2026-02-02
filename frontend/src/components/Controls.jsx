import React, { useState } from 'react';
import { SAMPLE_SCENARIOS } from '../services/scenarios';

const Controls = ({
    onLoadScenario,
    onStartNew,
    onExport,
    sessionData,
    apiLogs,
    showLogs,
    setShowLogs
}) => {
    const [selectedScenario, setSelectedScenario] = useState('Bank Fraud');

    const handleLoadScenario = () => {
        const scenario = SAMPLE_SCENARIOS[selectedScenario];
        if (scenario) {
            onLoadScenario(scenario);
        }
    };

    return (
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Test Controls</h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Scenario Selection */}
                <div className="flex flex-col">
                    <label className="text-sm font-semibold text-gray-700 mb-2">Select Test Scenario:</label>
                    <select
                        value={selectedScenario}
                        onChange={(e) => setSelectedScenario(e.target.value)}
                        className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white text-sm w-full text-gray-900"
                    >
                        {Object.keys(SAMPLE_SCENARIOS).map(scenarioName => (
                            <option key={scenarioName} value={scenarioName}>
                                {scenarioName}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Action Buttons */}
                <div className="flex flex-col">
                    <label className="text-sm font-semibold text-gray-700 mb-2">Actions:</label>
                    <div className="flex flex-wrap gap-2">
                        <button onClick={handleLoadScenario} className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors duration-200">
                            Load Scenario
                        </button>
                        <button onClick={onStartNew} className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors duration-200">
                            Start New Test
                        </button>
                        <button onClick={onExport} className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors duration-200">
                            Export Results
                        </button>
                    </div>
                </div>

                {/* View Controls */}
                <div className="flex flex-col">
                    <label className="text-sm font-semibold text-gray-700 mb-2">View Options:</label>
                    <button
                        onClick={() => setShowLogs(!showLogs)}
                        className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors duration-200 w-full"
                    >
                        {showLogs ? 'Hide' : 'View'} API Logs
                    </button>
                </div>
            </div>

            {/* API Logs Modal */}
            {showLogs && (
                <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
                    <div className="flex justify-between items-center mb-3">
                        <h4 className="font-semibold text-gray-800">API Request/Response Logs</h4>
                        <button onClick={() => setShowLogs(false)} className="text-gray-500 hover:text-gray-700">
                            ✕
                        </button>
                    </div>
                    <div className="max-h-96 overflow-y-auto space-y-3">
                        {apiLogs.length === 0 ? (
                            <p className="text-gray-500 text-sm">No API calls yet</p>
                        ) : (
                            apiLogs.map((log, idx) => (
                                <div key={idx} className="bg-white p-3 rounded border border-gray-200 text-xs">
                                    <div className="flex justify-between items-center mb-2">
                                        <span className="font-semibold">Request #{idx + 1}</span>
                                        <span className="text-xs text-gray-500">
                                            {new Date(log.timestamp).toLocaleTimeString()}
                                        </span>
                                    </div>
                                    <pre className="bg-gray-900 text-green-400 p-2 rounded overflow-x-auto text-xs font-mono">
                                        {JSON.stringify(log.request, null, 2)}
                                    </pre>
                                    <div className="flex justify-between items-center mb-2 mt-2">
                                        <span className="font-semibold">Response</span>
                                        <span className={`text-xs ${log.response.status === 'success' ? 'text-green-600' : 'text-red-600'}`}>
                                            {log.response.status}
                                        </span>
                                    </div>
                                    <pre className="bg-gray-900 text-green-400 p-2 rounded overflow-x-auto text-xs font-mono">
                                        {JSON.stringify(log.response, null, 2)}
                                    </pre>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Controls;
