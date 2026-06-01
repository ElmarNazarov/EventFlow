"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useAuth } from "@/features/auth/useAuth";
import { createInventoryItem, listInventory, updateInventoryItem } from "@/features/inventory/api";
import {
  createInventorySchema,
  type CreateInventoryFormValues,
} from "@/features/inventory/schemas";
import type { InventoryItem } from "@/features/inventory/types";
import { AppShell } from "@/shared/layouts/AppShell";
import { PageHeader } from "@/shared/components/PageHeader";
import { Button } from "@/shared/components/Button";
import { Input } from "@/shared/components/Input";
import { Card } from "@/shared/components/Card";
import { LoadingState } from "@/shared/components/LoadingState";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/shared/components/Table";

export default function InventoryPage() {
  const { canMutate } = useAuth();
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [editing, setEditing] = useState<InventoryItem | null>(null);

  const { data, isLoading } = useQuery({
    queryKey: ["inventory", search],
    queryFn: () => listInventory({ page: 1, page_size: 100, search: search || undefined }),
  });

  const createForm = useForm<CreateInventoryFormValues>({
    resolver: zodResolver(createInventorySchema),
    defaultValues: {
      sku: "",
      name: "",
      available_quantity: 0,
      reorder_level: 10,
      is_active: true,
    },
  });

  const createMutation = useMutation({
    mutationFn: createInventoryItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["inventory"] });
      setShowCreate(false);
      createForm.reset();
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, qty }: { id: number; qty: number }) =>
      updateInventoryItem(id, { available_quantity: qty }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["inventory"] });
      setEditing(null);
    },
  });

  return (
    <AppShell title="Inventory">
      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <PageHeader title="Inventory" description="Stock levels and SKU management" />
        {canMutate && (
          <Button onClick={() => setShowCreate(!showCreate)}>
            {showCreate ? "Cancel" : "Add item"}
          </Button>
        )}
      </div>

      <Input
        placeholder="Search SKU or name…"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="mb-6 max-w-sm"
      />

      {showCreate && canMutate && (
        <Card className="mb-6">
          <form
            onSubmit={createForm.handleSubmit((values) => createMutation.mutate(values))}
            className="grid gap-4 md:grid-cols-2"
          >
            <Input label="SKU" {...createForm.register("sku")} />
            <Input label="Name" {...createForm.register("name")} />
            <Input
              label="Available quantity"
              type="number"
              {...createForm.register("available_quantity")}
            />
            <Input
              label="Reorder level"
              type="number"
              {...createForm.register("reorder_level")}
            />
            <div className="md:col-span-2">
              <Button type="submit" disabled={createMutation.isPending}>
                Save item
              </Button>
            </div>
          </form>
        </Card>
      )}

      {isLoading && <LoadingState />}

      {data && (
        <Table>
          <TableHead>
            <TableRow>
              <TableHeader>SKU</TableHeader>
              <TableHeader>Name</TableHeader>
              <TableHeader>Available</TableHeader>
              <TableHeader>Reserved</TableHeader>
              <TableHeader>Reorder at</TableHeader>
              <TableHeader>Status</TableHeader>
              {canMutate && <TableHeader>Actions</TableHeader>}
            </TableRow>
          </TableHead>
          <TableBody>
            {data.items.map((item) => (
              <TableRow key={item.id}>
                <TableCell className="font-mono">{item.sku}</TableCell>
                <TableCell>{item.name}</TableCell>
                <TableCell>
                  {editing?.id === item.id ? (
                    <input
                      type="number"
                      className="w-20 rounded border border-slate-600 bg-slate-900 px-2 py-1 text-sm"
                      defaultValue={item.available_quantity}
                      onBlur={(e) => {
                        const qty = parseInt(e.target.value, 10);
                        if (!Number.isNaN(qty)) {
                          updateMutation.mutate({ id: item.id, qty });
                        } else {
                          setEditing(null);
                        }
                      }}
                      autoFocus
                    />
                  ) : (
                    <span
                      className={
                        item.available_quantity <= item.reorder_level
                          ? "text-amber-400"
                          : ""
                      }
                    >
                      {item.available_quantity}
                    </span>
                  )}
                </TableCell>
                <TableCell>{item.reserved_quantity}</TableCell>
                <TableCell>{item.reorder_level}</TableCell>
                <TableCell>{item.is_active ? "Active" : "Inactive"}</TableCell>
                {canMutate && (
                  <TableCell>
                    <Button variant="ghost" onClick={() => setEditing(item)}>
                      Edit qty
                    </Button>
                  </TableCell>
                )}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </AppShell>
  );
}
