import { apiClient } from "@/shared/api/client";
import type { Order, PaginatedOrders } from "./types";

export interface ListOrdersParams {
  page?: number;
  page_size?: number;
  status?: string;
  search?: string;
  ordering?: string;
}

export async function listOrders(params: ListOrdersParams = {}): Promise<PaginatedOrders> {
  const { data } = await apiClient.get<PaginatedOrders>("/orders", { params });
  return data;
}

export async function getOrder(orderId: number): Promise<Order> {
  const { data } = await apiClient.get<Order>(`/orders/${orderId}`);
  return data;
}

export async function createOrder(payload: {
  customer_name: string;
  customer_email: string;
  currency: string;
  items: { sku: string; quantity: number; unit_price?: number }[];
}): Promise<Order> {
  const { data } = await apiClient.post<Order>("/orders", payload);
  return data;
}
