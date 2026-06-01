"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useAuth } from "../useAuth";
import { loginSchema, type LoginFormValues } from "../schemas";
import { Button } from "@/shared/components/Button";
import { Input } from "@/shared/components/Input";

export function LoginForm() {
  const { login, loginError, isLoggingIn } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "admin@eventflow.local", password: "password123" },
  });

  return (
    <form onSubmit={handleSubmit((data) => login(data))} className="space-y-4">
      <Input
        label="Email"
        type="email"
        autoComplete="email"
        error={errors.email?.message}
        {...register("email")}
      />
      <Input
        label="Password"
        type="password"
        autoComplete="current-password"
        error={errors.password?.message}
        {...register("password")}
      />
      {loginError && (
        <p className="text-sm text-red-400">
          {loginError instanceof Error ? loginError.message : "Login failed"}
        </p>
      )}
      <Button type="submit" className="w-full" disabled={isLoggingIn}>
        {isLoggingIn ? "Signing in…" : "Sign in"}
      </Button>
    </form>
  );
}
