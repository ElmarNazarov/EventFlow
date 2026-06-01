import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EventFlow",
  description: "Event-driven order and workflow processing platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
