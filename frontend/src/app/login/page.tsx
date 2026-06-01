import { Card } from "@/shared/components/Card";
import { LoginForm } from "@/features/auth/components/LoginForm";

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-white">EventFlow</h1>
          <p className="mt-2 text-slate-400">Sign in to the operations dashboard</p>
        </div>
        <Card>
          <LoginForm />
          <p className="mt-6 text-center text-xs text-slate-500">
            Demo: admin@eventflow.local / password123
          </p>
        </Card>
      </div>
    </main>
  );
}
