// API configuration
const getApiBaseUrl = () => {
  // In production, use the environment variable or default to Render backend
  // Update this URL to your deployed Voice Clone Chat backend on Render
  let apiUrl = process.env.REACT_APP_API_URL || 'https://voice-clone-chat-backend.onrender.com/api';
  
  // Ensure the URL ends with /api
  if (!apiUrl.endsWith('/api')) {
    // If it doesn't end with /api, add it
    if (apiUrl.endsWith('/')) {
      apiUrl = apiUrl + 'api';
    } else {
      apiUrl = apiUrl + '/api';
    }
  }
  
  // Log for debugging
  console.log('API Base URL:', apiUrl);
  
  return apiUrl;
};

export const API_BASE_URL = getApiBaseUrl();

