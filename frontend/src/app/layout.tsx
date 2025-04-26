import { Poppins } from 'next/font/google';
import "./globals.css";
import { ReactNode } from "react";

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['400', '700'], // Add weights as needed
});

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={poppins.className}>
      <body>
        {children}
      </body>
    </html>
  );
}