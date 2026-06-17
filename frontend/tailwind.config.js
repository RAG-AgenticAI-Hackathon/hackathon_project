/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['Syne', 'sans-serif'],
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        bg: {
          primary: '#0D0D1A',
          secondary: '#111827',
          card: '#1A2035',
        },
        accent: '#2563EB',
      },
      keyframes: {
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        dotBounce: {
          '0%, 80%, 100%': { transform: 'translateY(0)', opacity: '0.5' },
          '40%': { transform: 'translateY(-8px)', opacity: '1' },
        },
      },
      animation: {
        'fade-up': 'fadeUp 0.3s cubic-bezier(0.4, 0, 0.2, 1) forwards',
        'dot-bounce': 'dotBounce 1.2s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
