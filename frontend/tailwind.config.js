// frontend/tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx}",    // include App Router files
    "./src/pages/**/*.{js,ts,jsx,tsx}",  // if you have pages
    "./src/components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        charcoal: "#2E353E",
        mint:     "#88D286",
        lemon:    "#D6E06B",
        carrot:   "#F87D4D",
      },
    },
  },
  plugins: [],
};
