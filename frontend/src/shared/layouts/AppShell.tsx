"use client";

import { useAuth } from "@/features/auth/useAuth";
import { LoadingState } from "@/shared/components/LoadingState";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

interface AppShellProps {
  children: React.ReactNode;
  title: string;
}

export function AppShell({ children, title }: AppShellProps) {
  const { isLoading, isAuthenticated } = useAuth();

  if (isLoading) {
    return <LoadingState message="Loading session…" />;
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex flex-1 flex-col">
        <Topbar title={title} />
        <main className="flex-1 overflow-auto p-6">{children}</main>
      </div>
    </div>
  );
}
