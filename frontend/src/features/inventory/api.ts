import { apiClient } from "@/shared/api/client";
import type { InventoryItem, PaginatedInventory } from "./types";

export async function listInventory(params: {
  page?: number;
  page_size?: number;
  search?: string;
} = {}): Promise<PaginatedInventory> {
  const { data } = await apiClient.get<PaginatedInventory>("/inventory", { params });
  return data;
}

export async function createInventoryItem(payload: {
  sku: string;
  name: string;
  available_quantity: number;
  reorder_level: number;
  is_active: boolean;
}): Promise<InventoryItem> {
  const { data } = await apiClient.post<InventoryItem>("/inventory", payload);
  return data;
}

export async function updateInventoryItem(
  id: number,
  payload: Partial<{
    name: string;
    available_quantity: number;
    reorder_level: number;
    is_active: boolean;
  }>,
): Promise<InventoryItem> {
  const { data } = await apiClient.patch<InventoryItem>(`/inventory/${id}`, payload);
  return data;
}
