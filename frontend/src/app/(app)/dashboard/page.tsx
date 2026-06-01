"use client";

import { useAuth } from "@/features/auth/useAuth";
import { Badge } from "@/shared/components/Badge";
import { Card } from "@/shared/components/Card";
import { PageHeader } from "@/shared/components/PageHeader";
import { AppShell } from "@/shared/layouts/AppShell";

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <AppShell title="Dashboard">
      <PageHeader
        title="Operations Dashboard"
        description="Welcome back. Analytics and workflows arrive in later milestones."
      />
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <p className="text-sm text-slate-400">Signed in as</p>
          <p className="mt-1 text-lg font-semibold text-white">{user?.full_name}</p>
          <p className="text-sm text-slate-500">{user?.email}</p>
          <div className="mt-3">{user?.role && <Badge label={user.role} />}</div>
        </Card>
        <Card>
          <p className="text-sm text-slate-400">Milestone 2</p>
          <p className="mt-1 text-white">Authentication &amp; app shell complete</p>
          <p className="mt-2 text-sm text-slate-500">
            Orders, workflows, and event streams coming in Milestone 3+.
          </p>
        </Card>
        <Card>
          <p className="text-sm text-slate-400">Your permissions</p>
          <p className="mt-2 text-sm text-slate-300">
            {user?.role === "VIEWER" || user?.role === "SUPPORT"
              ? "Read-only access to operational data."
              : "Can create and manage orders and inventory (from M3)."}
          </p>
        </Card>
      </div>
    </AppShell>
  );
}
