import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        hope: {
          DEFAULT: "#16A34A",
        },
        navy: {
          DEFAULT: "#0F1F3D",
        },
      },
    },
  },
  plugins: [],
};

export default config;
