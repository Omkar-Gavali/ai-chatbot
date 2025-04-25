// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        charcoal: "#2E353E",  // dark background
        mint:     "#88D286",  // fresh accent
        lemon:    "#D6E06B",  // highlight
        carrot:   "#F87D4D",  // call-to-action
      },
    },
  },
  plugins: [],
};
