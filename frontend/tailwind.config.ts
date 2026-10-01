import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#065f46',
          light: '#10b981',
          medium: '#059669',
        },
        accent: '#f59e0b',
        danger: '#ef4444',
        warning: '#f97316',
      },
      opacity: {
        15: '0.15',
        45: '0.45',
        65: '0.65',
      },
    },
  },
  plugins: [],
};
export default config;
