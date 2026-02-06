import axios from "axios";

// Use environment variable for API URL in production, or default to /api for dev
// If VITE_API_URL is set, use it directly. Otherwise use /api (relative to frontend domain)
// NOTE: VITE_API_URL should be the full backend URL with /api (e.g., https://backend.railway.app/api)
let API_BASE_URL = import.meta.env.VITE_API_URL || "/api";

// Normalize the URL
if (API_BASE_URL && API_BASE_URL !== "/api") {
  // If it's a full URL (starts with http:// or https://), use it as-is (but ensure it has /api)
  if (API_BASE_URL.startsWith("http://") || API_BASE_URL.startsWith("https://")) {
    // Already a full URL - ensure it ends with /api
    API_BASE_URL = API_BASE_URL.replace(/\/+$/, ""); // Remove trailing slashes
    if (!API_BASE_URL.endsWith("/api")) {
      API_BASE_URL = API_BASE_URL + "/api";
    }
  } else {
    // Not a full URL - it's likely just a domain without protocol
    // This means it should be treated as a relative path, but that's unusual
    // Better to assume they meant https://
    console.warn("⚠️ VITE_API_URL doesn't start with http:// or https://. Assuming https://");
    API_BASE_URL = API_BASE_URL.replace(/^\/+/, ""); // Remove leading slashes
    API_BASE_URL = `https://${API_BASE_URL}`;
    if (!API_BASE_URL.endsWith("/api")) {
      API_BASE_URL = API_BASE_URL + "/api";
    }
  }
}

console.log("🌐 API Base URL:", API_BASE_URL);
console.log("🌐 VITE_API_URL env var:", import.meta.env.VITE_API_URL);
console.log("🌐 Environment:", import.meta.env.MODE);

// Warn if using relative URL in production (might not work)
if (API_BASE_URL === "/api" && import.meta.env.MODE === "production") {
  console.warn("⚠️ Using relative API URL in production. Make sure frontend and backend are on the same domain, or set VITE_API_URL environment variable.");
}

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 second timeout (reduced from 30s)
  withCredentials: true, // Include cookies for CORS
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 errors (unauthorized) - token expired or invalid
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error.response?.status, error.response?.data || error.message);
    
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      // Redirect to login if not already there
      if (!window.location.pathname.includes("/login") && !window.location.pathname.includes("/register")) {
        window.location.href = "/login";
      }
    }
    
    // Log network errors with more detail
    if (!error.response) {
      if (error.code === 'ECONNABORTED') {
        console.error(`⏱️ Request timeout after ${error.config?.timeout || 10000}ms`);
        console.error(`🌐 Backend URL: ${API_BASE_URL}`);
        console.error(`💡 Check if backend is running and accessible`);
      } else if (error.code === 'ERR_NETWORK' || error.message.includes('Network Error')) {
        console.error("❌ Network error - cannot reach backend");
        console.error(`🌐 Backend URL: ${API_BASE_URL}`);
        console.error(`💡 Possible causes:`);
        console.error(`   - Backend is not running`);
        console.error(`   - CORS is blocking the request`);
        console.error(`   - Network connectivity issue`);
        console.error(`   - Backend URL is incorrect`);
      } else {
        console.error("❌ Network error:", error.message);
        console.error(`🌐 Backend URL: ${API_BASE_URL}`);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
