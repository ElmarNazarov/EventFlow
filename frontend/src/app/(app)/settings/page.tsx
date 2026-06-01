"use client";

import { useAuth } from "@/features/auth/useAuth";
import { Badge } from "@/shared/components/Badge";
import { Card } from "@/shared/components/Card";
import { PageHeader } from "@/shared/components/PageHeader";
import { AppShell } from "@/shared/layouts/AppShell";

export default function SettingsPage() {
  const { user } = useAuth();

  return (
    <AppShell title="Settings">
      <PageHeader title="Settings" description="Account and preferences" />
      <Card className="max-w-lg">
        <dl className="space-y-4 text-sm">
          <div>
            <dt className="text-slate-500">Full name</dt>
            <dd className="text-white">{user?.full_name}</dd>
          </div>
          <div>
            <dt className="text-slate-500">Email</dt>
            <dd className="text-white">{user?.email}</dd>
          </div>
          <div>
            <dt className="text-slate-500">Role</dt>
            <dd className="mt-1">{user?.role && <Badge label={user.role} />}</dd>
          </div>
          <div>
            <dt className="text-slate-500">Status</dt>
            <dd className="text-white">{user?.is_active ? "Active" : "Inactive"}</dd>
          </div>
        </dl>
      </Card>
    </AppShell>
  );
}
