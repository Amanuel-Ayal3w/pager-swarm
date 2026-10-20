import type { Metadata } from "next";
import localFont from "next/font/local";

import { Header } from "@/components/header";

import "./globals.css";

const sans = localFont({
  src: "./fonts/geist.woff2",
  variable: "--font-geist",
  weight: "100 900",
  display: "swap",
});

const pixel = localFont({
  src: "./fonts/geist-pixel.woff2",
  variable: "--font-geist-pixel",
  display: "swap",
});

const mono = localFont({
  src: "./fonts/geist-mono.woff2",
  variable: "--font-geist-mono",
  weight: "100 900",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Pager",
  description: "Incident response for the operator on call.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${sans.variable} ${pixel.variable} ${mono.variable}`}>
      <body className="bg-canvas font-sans text-ink antialiased">
        <Header />
        {children}
      </body>
    </html>
  );
}
