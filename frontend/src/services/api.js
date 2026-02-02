import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_KEY = import.meta.env.VITE_API_KEY || 'your_secret_key_here';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
  }
});

export const detectScam = async (sessionId, message, conversationHistory, metadata) => {
  try {
    const response = await apiClient.post('/api/detect-scam', {
      sessionId,
      message,
      conversationHistory,
      metadata
    });
    return response.data;
  } catch (error) {
    console.error('Error detecting scam:', error);
    throw error;
  }
};

export const getSession = async (sessionId) => {
  try {
    const response = await apiClient.get(`/api/session/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching session:', error);
    throw error;
  }
};

export const resetSession = async (sessionId) => {
  try {
    const response = await apiClient.post(`/api/reset-session/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error resetting session:', error);
    throw error;
  }
};

export default apiClient;
