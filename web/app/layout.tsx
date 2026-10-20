import type { Metadata } from "next";
import localFont from "next/font/local";
import Script from "next/script";

import { LiveProvider } from "@/components/live";
import { Shell } from "@/components/shell";

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
    <html lang="en" className={`${sans.variable} ${pixel.variable} ${mono.variable}`} suppressHydrationWarning>
      <body className="bg-canvas font-sans text-ink antialiased">
        <Script id="pager-theme" strategy="beforeInteractive">
          {`try{if(localStorage.getItem("pager-theme")==="light")document.documentElement.dataset.theme="light"}catch(e){}`}
        </Script>
        <LiveProvider>
          <Shell>{children}</Shell>
        </LiveProvider>
      </body>
    </html>
  );
}
