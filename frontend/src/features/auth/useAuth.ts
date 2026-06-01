"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import * as authApi from "./api";
import { clearAuthToken, getAuthToken, setAuthToken } from "./token";
import type { LoginFormValues } from "./schemas";

export function useAuth() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [hasToken, setHasToken] = useState(false);

  useEffect(() => {
    setHasToken(!!getAuthToken());
  }, []);

  const userQuery = useQuery({
    queryKey: ["auth", "me"],
    queryFn: authApi.getCurrentUser,
    enabled: hasToken,
    retry: false,
  });

  const loginMutation = useMutation({
    mutationFn: (values: LoginFormValues) => authApi.login(values.email, values.password),
    onSuccess: (data) => {
      setAuthToken(data.access_token);
      setHasToken(true);
      queryClient.invalidateQueries({ queryKey: ["auth", "me"] });
      router.push("/dashboard");
      router.refresh();
    },
  });

  const logoutMutation = useMutation({
    mutationFn: async () => {
      try {
        await authApi.logout();
      } finally {
        clearAuthToken();
        queryClient.clear();
      }
    },
    onSuccess: () => {
      router.push("/login");
      router.refresh();
    },
  });

  return {
    user: userQuery.data,
    isLoading: userQuery.isLoading,
    isAuthenticated: !!userQuery.data,
    login: loginMutation.mutate,
    loginError: loginMutation.error,
    isLoggingIn: loginMutation.isPending,
    logout: logoutMutation.mutate,
    isLoggingOut: logoutMutation.isPending,
  };
}
