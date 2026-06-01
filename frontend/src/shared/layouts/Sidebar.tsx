"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Bell,
  Boxes,
  GitBranch,
  LayoutDashboard,
  Package,
  Radio,
  Settings,
} from "lucide-react";
import { cn } from "@/shared/utils/cn";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/orders", label: "Orders", icon: Package },
  { href: "/workflows", label: "Workflows", icon: GitBranch, disabled: true },
  { href: "/events", label: "Events", icon: Radio, disabled: true },
  { href: "/inventory", label: "Inventory", icon: Boxes },
  { href: "/notifications", label: "Notifications", icon: Bell, disabled: true },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex w-64 flex-col border-r border-slate-700/50 bg-slate-900/50">
      <div className="border-b border-slate-700/50 px-6 py-5">
        <Link href="/dashboard" className="text-lg font-bold text-white">
          EventFlow
        </Link>
        <p className="text-xs text-slate-500">Operations Platform</p>
      </div>
      <nav className="flex-1 space-y-1 p-4">
        {navItems.map(({ href, label, icon: Icon, disabled }) => (
          <Link
            key={href}
            href={disabled ? "#" : href}
            className={cn(
              "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
              pathname === href
                ? "bg-sky-600/20 text-sky-300"
                : "text-slate-400 hover:bg-slate-800 hover:text-white",
              disabled && "pointer-events-none opacity-40",
            )}
            aria-disabled={disabled}
          >
            <Icon className="h-4 w-4" />
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
