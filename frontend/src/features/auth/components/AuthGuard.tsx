"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { getAuthToken } from "../token";
import { useAuth } from "../useAuth";
import { LoadingState } from "@/shared/components/LoadingState";

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { isLoading, isAuthenticated, user } = useAuth();

  useEffect(() => {
    const token = getAuthToken();
    if (!token) {
      router.replace("/login");
    }
  }, [router]);

  useEffect(() => {
    if (!isLoading && !isAuthenticated && !getAuthToken()) {
      router.replace("/login");
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading || !user) {
    return <LoadingState message="Verifying session…" />;
  }

  return <>{children}</>;
}
