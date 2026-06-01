import { apiClient } from "@/shared/api/client";
import type { LoginResponse, User } from "./types";

export async function login(email: string, password: string): Promise<LoginResponse> {
  const { data } = await apiClient.post<LoginResponse>("/auth/login", { email, password });
  return data;
}

export async function logout(): Promise<void> {
  await apiClient.post("/auth/logout");
}

export async function getCurrentUser(): Promise<User> {
  const { data } = await apiClient.get<User>("/auth/me");
  return data;
}
