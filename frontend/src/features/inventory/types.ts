export interface InventoryItem {
  id: number;
  sku: string;
  name: string;
  available_quantity: number;
  reserved_quantity: number;
  reorder_level: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface PaginatedInventory {
  items: InventoryItem[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}
