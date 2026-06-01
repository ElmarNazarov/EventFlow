import { cn } from "@/shared/utils/cn";

const roleStyles: Record<string, string> = {
  ADMIN: "bg-purple-500/20 text-purple-300",
  OPS_MANAGER: "bg-sky-500/20 text-sky-300",
  SUPPORT: "bg-amber-500/20 text-amber-300",
  VIEWER: "bg-slate-500/20 text-slate-300",
};

export function Badge({ label, className }: { label: string; className?: string }) {
  return (
    <span
      className={cn(
        "inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium",
        roleStyles[label] ?? "bg-slate-500/20 text-slate-300",
        className,
      )}
    >
      {label.replace("_", " ")}
    </span>
  );
}
