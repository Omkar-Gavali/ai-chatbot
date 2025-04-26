// tailwind.config.js
module.exports = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
    "./src/pages/**/*.{js,ts,jsx,tsx}",
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
