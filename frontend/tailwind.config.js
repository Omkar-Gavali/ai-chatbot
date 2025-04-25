/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./app/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        charcoal: "#2e353e",  // dark background
        mint:     "#88d286",  // fresh accent
        lemon:    "#D6E06B",  // highlight
        carrot:   "#f87d4d",  // call-to-action
      },
    },
  },
  plugins: [],
};
