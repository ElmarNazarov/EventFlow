"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { use } from "react";
import { getOrder } from "@/features/orders/api";
import { AppShell } from "@/shared/layouts/AppShell";
import { PageHeader } from "@/shared/components/PageHeader";
import { Card } from "@/shared/components/Card";
import { LoadingState } from "@/shared/components/LoadingState";
import { OrderStatusBadge } from "@/shared/components/OrderStatusBadge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/shared/components/Table";
import { formatMoney } from "@/shared/utils/formatMoney";
import { formatDate } from "@/shared/utils/formatDate";

export default function OrderDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const orderId = parseInt(id, 10);

  const { data: order, isLoading, error } = useQuery({
    queryKey: ["orders", orderId],
    queryFn: () => getOrder(orderId),
    enabled: !Number.isNaN(orderId),
  });

  return (
    <AppShell title="Order detail">
      <Link href="/orders" className="mb-4 inline-block text-sm text-sky-400 hover:text-sky-300">
        ← Back to orders
      </Link>

      {isLoading && <LoadingState />}
      {error && (
        <p className="text-red-400">
          {error instanceof Error ? error.message : "Failed to load order"}
        </p>
      )}

      {order && (
        <>
          <PageHeader
            title={order.order_number}
            description={`${order.customer_name} · ${order.customer_email}`}
          />

          <div className="mb-6 grid gap-4 md:grid-cols-3">
            <Card>
              <p className="text-sm text-slate-400">Status</p>
              <div className="mt-2">
                <OrderStatusBadge status={order.status} />
              </div>
            </Card>
            <Card>
              <p className="text-sm text-slate-400">Total</p>
              <p className="mt-2 text-xl font-semibold text-white">
                {formatMoney(order.total_amount, order.currency)}
              </p>
            </Card>
            <Card>
              <p className="text-sm text-slate-400">Created</p>
              <p className="mt-2 text-white">{formatDate(order.created_at)}</p>
            </Card>
          </div>

          <h3 className="mb-3 font-medium text-white">Line items</h3>
          <Table>
            <TableHead>
              <TableRow>
                <TableHeader>SKU</TableHeader>
                <TableHeader>Product</TableHeader>
                <TableHeader>Qty</TableHeader>
                <TableHeader>Unit price</TableHeader>
                <TableHeader>Total</TableHeader>
              </TableRow>
            </TableHead>
            <TableBody>
              {(order.items ?? []).map((item) => (
                <TableRow key={item.id}>
                  <TableCell className="font-mono text-sm">{item.sku}</TableCell>
                  <TableCell>{item.product_name}</TableCell>
                  <TableCell>{item.quantity}</TableCell>
                  <TableCell>{formatMoney(item.unit_price, order.currency)}</TableCell>
                  <TableCell>{formatMoney(item.total_price, order.currency)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </>
      )}
    </AppShell>
  );
}
