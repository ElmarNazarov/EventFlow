"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { useAuth } from "@/features/auth/useAuth";
import { listOrders } from "@/features/orders/api";
import { AppShell } from "@/shared/layouts/AppShell";
import { PageHeader } from "@/shared/components/PageHeader";
import { Button } from "@/shared/components/Button";
import { Input } from "@/shared/components/Input";
import { Select } from "@/shared/components/Select";
import { LoadingState } from "@/shared/components/LoadingState";
import { EmptyState } from "@/shared/components/EmptyState";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/shared/components/Table";
import { OrderStatusBadge } from "@/shared/components/OrderStatusBadge";
import { formatMoney } from "@/shared/utils/formatMoney";
import { formatDate } from "@/shared/utils/formatDate";

export default function OrdersPage() {
  const { canMutate } = useAuth();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");

  const { data, isLoading, error } = useQuery({
    queryKey: ["orders", page, search, status],
    queryFn: () =>
      listOrders({
        page,
        search: search || undefined,
        status: status || undefined,
        ordering: "-created_at",
      }),
  });

  return (
    <AppShell title="Orders">
      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <PageHeader
          title="Orders"
          description="Manage customer orders and fulfillment pipeline"
        />
        {canMutate && (
          <Link href="/orders/new">
            <Button>Create order</Button>
          </Link>
        )}
      </div>

      <div className="mb-6 flex flex-wrap gap-3">
        <Input
          placeholder="Search order #, customer…"
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
          className="max-w-xs"
        />
        <Select
          value={status}
          onChange={(e) => {
            setStatus(e.target.value);
            setPage(1);
          }}
          className="max-w-[200px]"
        >
          <option value="">All statuses</option>
          <option value="CREATED">Created</option>
          <option value="INVENTORY_PENDING">Inventory pending</option>
          <option value="COMPLETED">Completed</option>
          <option value="FAILED">Failed</option>
          <option value="CANCELLED">Cancelled</option>
        </Select>
      </div>

      {isLoading && <LoadingState />}
      {error && (
        <p className="text-red-400">
          {error instanceof Error ? error.message : "Failed to load orders"}
        </p>
      )}
      {data && data.items.length === 0 && (
        <EmptyState title="No orders found" description="Create your first order to get started." />
      )}
      {data && data.items.length > 0 && (
        <>
          <Table>
            <TableHead>
              <TableRow>
                <TableHeader>Order #</TableHeader>
                <TableHeader>Customer</TableHeader>
                <TableHeader>Status</TableHeader>
                <TableHeader>Total</TableHeader>
                <TableHeader>Created</TableHeader>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.items.map((order) => (
                <TableRow key={order.id}>
                  <TableCell>
                    <Link
                      href={`/orders/${order.id}`}
                      className="font-medium text-sky-400 hover:text-sky-300"
                    >
                      {order.order_number}
                    </Link>
                  </TableCell>
                  <TableCell>
                    <div>{order.customer_name}</div>
                    <div className="text-xs text-slate-500">{order.customer_email}</div>
                  </TableCell>
                  <TableCell>
                    <OrderStatusBadge status={order.status} />
                  </TableCell>
                  <TableCell>{formatMoney(order.total_amount, order.currency)}</TableCell>
                  <TableCell className="text-slate-400">{formatDate(order.created_at)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <div className="mt-4 flex items-center justify-between text-sm text-slate-400">
            <span>
              Page {data.page} of {data.pages || 1} ({data.total} total)
            </span>
            <div className="flex gap-2">
              <Button
                variant="secondary"
                disabled={page <= 1}
                onClick={() => setPage((p) => p - 1)}
              >
                Previous
              </Button>
              <Button
                variant="secondary"
                disabled={page >= (data.pages || 1)}
                onClick={() => setPage((p) => p + 1)}
              >
                Next
              </Button>
            </div>
          </div>
        </>
      )}
    </AppShell>
  );
}
