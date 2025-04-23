// frontend/src/app/layout.tsx
import Script from 'next/script';
import './globals.css';           // your Tailwind import or other global CSS
import { Analytics } from "@vercel/analytics/react"

export const metadata = {
  title: 'My Chatbot',
  description: 'AI-powered beauty & nutrition advisor',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head />
      <body>
        {children}
        <Analytics />
        {/* Tailwind CSS via CDN with Next.js Script */}
        <Script
          src="https://cdn.tailwindcss.com"
          strategy="beforeInteractive"
        />
      </body>
    </html>
  );
}
