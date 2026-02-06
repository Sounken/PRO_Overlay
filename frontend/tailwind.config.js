/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3498db',
        secondary: '#2ecc71',
        danger: '#e74c3c',
        background: {
          start: '#1e1e2e',
          end: '#0f0f1e',
        },
        surface: '#2a2a3e',
        sidebar: '#16213e',
      },
      backgroundImage: {
        'gradient-main': 'linear-gradient(135deg, #1e1e2e 0%, #0f0f1e 100%)',
      },
    },
  },
  plugins: [],
}
