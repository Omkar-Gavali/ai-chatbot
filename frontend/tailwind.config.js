/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      './src/**/*.{js,ts,jsx,tsx}',
      './public/index.html',
    ],
    theme: {
      extend: {
        colors: {
          darkbg: '#2e353e',  // deep slate
          mint:   '#88d286',  // fresh mint
          lemon:  '#D6E06b',  // sunny yellow
          coral:  '#f87d4d',  // warm coral
        },
      },
    },
    plugins: [],
  };
  