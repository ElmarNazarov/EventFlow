import { AuthGuard } from "@/features/auth/components/AuthGuard";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return <AuthGuard>{children}</AuthGuard>;
}
