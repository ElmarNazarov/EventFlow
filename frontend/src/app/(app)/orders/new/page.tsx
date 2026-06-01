"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/features/auth/useAuth";
import { CreateOrderForm } from "@/features/orders/components/CreateOrderForm";
import { AppShell } from "@/shared/layouts/AppShell";
import { PageHeader } from "@/shared/components/PageHeader";
import { Card } from "@/shared/components/Card";

export default function NewOrderPage() {
  const router = useRouter();
  const { canMutate, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && !canMutate) {
      router.replace("/orders");
    }
  }, [canMutate, isLoading, router]);

  if (!canMutate) return null;

  return (
    <AppShell title="New order">
      <PageHeader title="Create order" description="Add customer details and line items" />
      <Card>
        <CreateOrderForm />
      </Card>
    </AppShell>
  );
}
