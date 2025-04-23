// frontend/src/pages/_document.tsx
import { Html, Head, Main, NextScript } from 'next/document';
import Script from 'next/script';

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        {/* Other head tags */}
      </Head>
      <body>
        <Main />
        <NextScript />
        {/* Tailwind via CDN using Next.js Script */}
        <Script
          src="https://cdn.tailwindcss.com"
          strategy="beforeInteractive"
        />
      </body>
    </Html>
  );
}
