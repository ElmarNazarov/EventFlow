import { cn } from "@/shared/utils/cn";

const statusStyles: Record<string, string> = {
  CREATED: "bg-slate-500/20 text-slate-300",
  INVENTORY_PENDING: "bg-blue-500/20 text-blue-300",
  INVENTORY_RESERVED: "bg-emerald-500/20 text-emerald-300",
  PAYMENT_PENDING: "bg-blue-500/20 text-blue-300",
  PAYMENT_CONFIRMED: "bg-emerald-500/20 text-emerald-300",
  PAYMENT_FAILED: "bg-red-500/20 text-red-300",
  SHIPPING_PENDING: "bg-blue-500/20 text-blue-300",
  SHIPPED: "bg-purple-500/20 text-purple-300",
  COMPLETED: "bg-emerald-500/20 text-emerald-300",
  CANCELLED: "bg-slate-700/50 text-slate-400",
  FAILED: "bg-red-500/20 text-red-300",
};

export function OrderStatusBadge({ status }: { status: string }) {
  return (
    <span
      className={cn(
        "inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium",
        statusStyles[status] ?? "bg-slate-500/20 text-slate-300",
      )}
    >
      {status.replace(/_/g, " ")}
    </span>
  );
}
