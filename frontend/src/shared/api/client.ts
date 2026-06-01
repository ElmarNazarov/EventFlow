import axios from "axios";
import { TOKEN_STORAGE_KEY } from "@/features/auth/types";

const baseURL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

apiClient.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
      document.cookie = "eventflow_token=; path=/; max-age=0";
      if (!window.location.pathname.startsWith("/login")) {
        window.location.href = "/login";
      }
    }
    const detail = error.response?.data?.detail;
    if (detail) {
      const message = typeof detail === "string" ? detail : JSON.stringify(detail);
      return Promise.reject(new Error(message));
    }
    return Promise.reject(error);
  },
);
