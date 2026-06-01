import { HTMLAttributes } from "react";
import { cn } from "@/shared/utils/cn";

export function Card({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "rounded-xl border border-slate-700/50 bg-slate-800/40 p-6 shadow-lg backdrop-blur",
        className,
      )}
      {...props}
    />
  );
}
