import { ButtonHTMLAttributes, forwardRef } from "react";
import { cn } from "@/shared/utils/cn";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-lg px-4 py-2 text-sm font-medium transition-colors disabled:opacity-50",
          variant === "primary" && "bg-sky-600 text-white hover:bg-sky-500",
          variant === "secondary" &&
            "border border-slate-600 bg-slate-800 text-slate-100 hover:bg-slate-700",
          variant === "ghost" && "text-slate-300 hover:bg-slate-800 hover:text-white",
          className,
        )}
        {...props}
      />
    );
  },
);
Button.displayName = "Button";
