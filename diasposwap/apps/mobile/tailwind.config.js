/** DiaspoSwap design tokens. Palette from the brand brief. */
module.exports = {
  content: ['./src/**/*.{ts,tsx}'],
  presets: [require('nativewind/preset')],
  darkMode: 'media',
  theme: {
    extend: {
      colors: {
        petrol: { DEFAULT: '#082F35', 700: '#0D3E45', 600: '#14505A' },
        emerald: { DEFAULT: '#087F6D', 100: '#D7EEE9', 300: '#5FB7A8' },
        gold: { DEFAULT: '#C9A44C', 100: '#F4EAD0', 700: '#8A6A1F' },
        ivory: { DEFAULT: '#FAF8F2', 200: '#EFEBDF', 300: '#E2DCCB' },
        anthracite: { DEFAULT: '#182525', 500: '#4A5858', 400: '#6B7878' },
        danger: { DEFAULT: '#A8432A', 100: '#F6E1DA' },
      },
      borderRadius: { xl: '14px', '2xl': '20px' },
    },
  },
  plugins: [],
};
