export type UserRole = "ADMIN" | "OPS_MANAGER" | "SUPPORT" | "VIEWER";

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const TOKEN_STORAGE_KEY = "eventflow_token";
export const TOKEN_COOKIE_NAME = "eventflow_token";
