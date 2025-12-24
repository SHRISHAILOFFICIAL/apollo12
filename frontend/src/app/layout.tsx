import type { Metadata } from "next";
import { Outfit, Inter } from "next/font/google";
import "./globals.css";
import "katex/dist/katex.min.css";

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-outfit",
  display: "swap",
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "DCET Prep - Mock Test Platform",
  description: "Prepare for DCET with our comprehensive mock test platform",
  icons: {
    icon: '/logo.jpg',
    apple: '/logo.jpg',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${outfit.variable} ${inter.variable} antialiased font-sans bg-background text-foreground`}>
        {children}
      </body>
    </html>
  );
}
