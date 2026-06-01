"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useFieldArray, useForm } from "react-hook-form";
import { listInventory } from "@/features/inventory/api";
import { createOrder } from "../api";
import { createOrderSchema, type CreateOrderFormValues } from "../schemas";
import { Button } from "@/shared/components/Button";
import { Input } from "@/shared/components/Input";
import { Select } from "@/shared/components/Select";

export function CreateOrderForm() {
  const router = useRouter();
  const queryClient = useQueryClient();

  const inventoryQuery = useQuery({
    queryKey: ["inventory", "all"],
    queryFn: () => listInventory({ page_size: 100 }),
  });

  const {
    register,
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateOrderFormValues>({
    resolver: zodResolver(createOrderSchema),
    defaultValues: {
      customer_name: "",
      customer_email: "",
      currency: "USD",
      items: [{ sku: "", quantity: 1, unit_price: 99.99 }],
    },
  });

  const { fields, append, remove } = useFieldArray({ control, name: "items" });

  const mutation = useMutation({
    mutationFn: createOrder,
    onSuccess: (order) => {
      queryClient.invalidateQueries({ queryKey: ["orders"] });
      router.push(`/orders/${order.id}`);
    },
  });

  const skus = inventoryQuery.data?.items ?? [];

  return (
    <form
      onSubmit={handleSubmit((data) =>
        mutation.mutate({
          ...data,
          items: data.items.map((item) => ({
            sku: item.sku,
            quantity: item.quantity,
            unit_price: item.unit_price,
          })),
        }),
      )}
      className="space-y-6"
    >
      <div className="grid gap-4 md:grid-cols-2">
        <Input
          label="Customer name"
          error={errors.customer_name?.message}
          {...register("customer_name")}
        />
        <Input
          label="Customer email"
          type="email"
          error={errors.customer_email?.message}
          {...register("customer_email")}
        />
        <Input label="Currency" maxLength={3} {...register("currency")} />
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-medium text-white">Line items</h3>
          <Button
            type="button"
            variant="secondary"
            onClick={() => append({ sku: "", quantity: 1, unit_price: 99.99 })}
          >
            Add item
          </Button>
        </div>
        {fields.map((field, index) => (
          <div
            key={field.id}
            className="grid gap-3 rounded-lg border border-slate-700/50 bg-slate-900/30 p-4 md:grid-cols-4"
          >
            <Select label="SKU" {...register(`items.${index}.sku`)}>
              <option value="">Select SKU</option>
              {skus.map((item) => (
                <option key={item.sku} value={item.sku}>
                  {item.sku} — {item.name} ({item.available_quantity} avail.)
                </option>
              ))}
            </Select>
            <Input
              label="Quantity"
              type="number"
              min={1}
              {...register(`items.${index}.quantity`)}
            />
            <Input
              label="Unit price"
              type="number"
              step="0.01"
              {...register(`items.${index}.unit_price`)}
            />
            {fields.length > 1 && (
              <div className="flex items-end">
                <Button type="button" variant="ghost" onClick={() => remove(index)}>
                  Remove
                </Button>
              </div>
            )}
          </div>
        ))}
        {errors.items?.message && (
          <p className="text-sm text-red-400">{String(errors.items.message)}</p>
        )}
      </div>

      {mutation.error && (
        <p className="text-sm text-red-400">
          {mutation.error instanceof Error ? mutation.error.message : "Failed to create order"}
        </p>
      )}

      <div className="flex gap-3">
        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? "Creating…" : "Create order"}
        </Button>
        <Button type="button" variant="secondary" onClick={() => router.push("/orders")}>
          Cancel
        </Button>
      </div>
    </form>
  );
}
