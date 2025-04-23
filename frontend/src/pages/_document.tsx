// frontend/src/pages/_document.tsx

import { Html, Head, Main, NextScript } from 'next/document';
import Script from 'next/script';

export default function Document() {
  return (
    <Html lang="en">
      <Head>{/* other meta tags */}</Head>
      <body>
        <Main />
        <NextScript />
+       <Script
           src="https://cdn.tailwindcss.com"
           strategy="beforeInteractive"
         />
      </body>
    </Html>
  );
}
