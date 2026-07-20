import type { Config } from "tailwindcss";

/**
 * Charte visuelle ATEN — « Le disque solaire »
 * navy (fondation, autorité) / or (soleil, valeur) / vert (renouvelable, climat)
 */
const config: Config = {
  content: [
    "./src/app/**/*.{ts,tsx}",
    "./src/components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: "#0A1E3F",
          50: "#EAEEF5",
          100: "#C9D3E6",
          200: "#93A6C6",
          300: "#5D77A3",
          400: "#2F4C7A",
          500: "#16305C",
          600: "#0F2650",
          700: "#0A1E3F",
          800: "#07162F",
          900: "#040D1D",
        },
        gold: {
          DEFAULT: "#C9A227",
          50: "#FBF6E7",
          100: "#F4E7BD",
          200: "#E9D084",
          300: "#DDBA4F",
          400: "#D0A833",
          500: "#C9A227",
          600: "#A9871C",
          700: "#836819",
          800: "#5C4913",
          900: "#3A2E0C",
        },
        vert: {
          DEFAULT: "#1FA36A",
          50: "#E7F7EF",
          100: "#C2ECD7",
          200: "#8CDBB4",
          300: "#52C78E",
          400: "#2BB377",
          500: "#1FA36A",
          600: "#178A5A",
          700: "#126B47",
          800: "#0D4C33",
          900: "#08301F",
        },
      },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 2px rgba(10,30,63,0.06), 0 8px 24px rgba(10,30,63,0.08)",
      },
    },
  },
  plugins: [],
};

export default config;
