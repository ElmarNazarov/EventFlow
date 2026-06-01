export type OrderStatus =
  | "CREATED"
  | "INVENTORY_PENDING"
  | "INVENTORY_RESERVED"
  | "PAYMENT_PENDING"
  | "PAYMENT_CONFIRMED"
  | "PAYMENT_FAILED"
  | "SHIPPING_PENDING"
  | "SHIPPED"
  | "COMPLETED"
  | "CANCELLED"
  | "FAILED";

export interface OrderItem {
  id: number;
  sku: string;
  product_name: string;
  quantity: number;
  unit_price: string;
  total_price: string;
  created_at: string;
}

export interface Order {
  id: number;
  order_number: string;
  customer_name: string;
  customer_email: string;
  status: OrderStatus;
  total_amount: string;
  currency: string;
  created_by_id: number;
  created_at: string;
  updated_at: string;
  items?: OrderItem[];
}

export interface PaginatedOrders {
  items: Order[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}
