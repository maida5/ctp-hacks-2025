// src/lib/api.js

// Reads backend API base URL from your .env file (fallback to localhost:8000)
export const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
