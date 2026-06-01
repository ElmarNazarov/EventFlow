import { TOKEN_COOKIE_NAME, TOKEN_STORAGE_KEY } from "./types";

export function setAuthToken(token: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem(TOKEN_STORAGE_KEY, token);
  document.cookie = `${TOKEN_COOKIE_NAME}=${token}; path=/; max-age=${60 * 60 * 24}; SameSite=Lax`;
}

export function clearAuthToken() {
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_STORAGE_KEY);
  document.cookie = `${TOKEN_COOKIE_NAME}=; path=/; max-age=0`;
}

export function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_STORAGE_KEY);
}
