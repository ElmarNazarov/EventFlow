import { z } from "zod";

export const createInventorySchema = z.object({
  sku: z.string().min(1, "SKU is required"),
  name: z.string().min(1, "Name is required"),
  available_quantity: z.coerce.number().int().min(0),
  reorder_level: z.coerce.number().int().min(0).default(0),
  is_active: z.boolean().default(true),
});

export const updateInventorySchema = z.object({
  name: z.string().min(1).optional(),
  available_quantity: z.coerce.number().int().min(0).optional(),
  reorder_level: z.coerce.number().int().min(0).optional(),
  is_active: z.boolean().optional(),
});

export type CreateInventoryFormValues = z.infer<typeof createInventorySchema>;
export type UpdateInventoryFormValues = z.infer<typeof updateInventorySchema>;
