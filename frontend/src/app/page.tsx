import { HealthStatus } from "@/components/HealthStatus";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-6 py-16">
      <div className="w-full max-w-2xl rounded-2xl border border-slate-700/50 bg-slate-800/40 p-10 shadow-2xl backdrop-blur">
        <p className="mb-2 text-sm font-medium uppercase tracking-widest text-sky-400">
          Milestone 1
        </p>
        <h1 className="mb-4 text-4xl font-bold tracking-tight text-white">EventFlow</h1>
        <p className="mb-8 text-slate-300">
          Event-driven order and workflow processing platform. Foundation stack is running —
          authentication and dashboard arrive in Milestone 2.
        </p>

        <HealthStatus />

        <div className="mt-8 flex flex-wrap gap-4 text-sm text-slate-400">
          <a
            href={`${process.env.NEXT_PUBLIC_API_BASE_URL?.replace("/api/v1", "") ?? "http://localhost:8000"}/docs`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sky-400 hover:text-sky-300"
          >
            API Docs →
          </a>
          <a
            href="http://localhost:15672"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sky-400 hover:text-sky-300"
          >
            RabbitMQ UI →
          </a>
          <a
            href="http://localhost:8080"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sky-400 hover:text-sky-300"
          >
            Kafka UI →
          </a>
        </div>
      </div>
    </main>
  );
}
