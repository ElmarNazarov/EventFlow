"use client";

import { ChevronDown, LogOut, User } from "lucide-react";
import { useState } from "react";
import { useAuth } from "@/features/auth/useAuth";
import { Badge } from "@/shared/components/Badge";

interface TopbarProps {
  title: string;
}

export function Topbar({ title }: TopbarProps) {
  const { user, logout, isLoggingOut } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-700/50 bg-slate-900/30 px-6">
      <h2 className="text-lg font-semibold text-white">{title}</h2>
      <div className="relative">
        <button
          type="button"
          onClick={() => setMenuOpen(!menuOpen)}
          className="flex items-center gap-2 rounded-lg border border-slate-600 bg-slate-800 px-3 py-1.5 text-sm text-slate-200 hover:bg-slate-700"
        >
          <User className="h-4 w-4" />
          <span className="hidden sm:inline">{user?.full_name ?? "User"}</span>
          {user?.role && <Badge label={user.role} />}
          <ChevronDown className="h-4 w-4 text-slate-400" />
        </button>
        {menuOpen && (
          <>
            <div className="fixed inset-0 z-10" onClick={() => setMenuOpen(false)} />
            <div className="absolute right-0 z-20 mt-2 w-48 rounded-lg border border-slate-600 bg-slate-800 py-1 shadow-xl">
              <div className="border-b border-slate-600 px-4 py-2 text-xs text-slate-400">
                {user?.email}
              </div>
              <button
                type="button"
                onClick={() => logout()}
                disabled={isLoggingOut}
                className="flex w-full items-center gap-2 px-4 py-2 text-sm text-slate-200 hover:bg-slate-700"
              >
                <LogOut className="h-4 w-4" />
                Sign out
              </button>
            </div>
          </>
        )}
      </div>
    </header>
  );
}
