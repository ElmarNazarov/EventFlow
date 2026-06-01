"use client";

import { useEffect, useState } from "react";
import { apiClient } from "@/shared/api/client";

interface HealthResponse {
  status: string;
  app: string;
  environment: string;
  checks: Record<string, string>;
}

export function HealthStatus() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient
      .get<HealthResponse>("/health")
      .then((res) => setHealth(res.data))
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to reach API"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="rounded-lg border border-slate-600 bg-slate-900/50 p-4 text-slate-400">
        Checking API health…
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-red-500/50 bg-red-950/30 p-4 text-red-300">
        API unreachable: {error}
      </div>
    );
  }

  if (!health) return null;

  return (
    <div className="rounded-lg border border-slate-600 bg-slate-900/50 p-4">
      <div className="mb-3 flex items-center gap-2">
        <span
          className={`inline-block h-2.5 w-2.5 rounded-full ${
            health.status === "ok" ? "bg-emerald-400" : "bg-amber-400"
          }`}
        />
        <span className="font-medium text-white">
          API {health.status === "ok" ? "healthy" : health.status}
        </span>
        <span className="text-slate-500">· {health.environment}</span>
      </div>
      <dl className="grid grid-cols-2 gap-2 text-sm">
        {Object.entries(health.checks).map(([key, value]) => (
          <div key={key} className="flex justify-between gap-4">
            <dt className="text-slate-400">{key}</dt>
            <dd
              className={
                value === "ok"
                  ? "text-emerald-400"
                  : value === "error"
                    ? "text-red-400"
                    : "text-slate-400"
              }
            >
              {value}
            </dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
