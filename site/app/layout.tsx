import type { ReactNode } from "react";
import "./globals.css";

export const metadata = {
  title: "CSC308 Agentic Lab — 2026 Postseason Statcast",
  description: "A site built and maintained by a team of AI agents, live in class.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
