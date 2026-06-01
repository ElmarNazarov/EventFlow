import { z } from "zod";

export const orderItemSchema = z.object({
  sku: z.string().min(1, "SKU is required"),
  quantity: z.coerce.number().int().min(1, "Min quantity is 1"),
  unit_price: z.coerce.number().positive().optional(),
});

export const createOrderSchema = z.object({
  customer_name: z.string().min(1, "Customer name is required"),
  customer_email: z.string().email("Valid email required"),
  currency: z.string().length(3).default("USD"),
  items: z.array(orderItemSchema).min(1, "Add at least one line item"),
});

export type CreateOrderFormValues = z.infer<typeof createOrderSchema>;
