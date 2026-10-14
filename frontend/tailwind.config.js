/** =========================================================
 * frontend/tailwind.config.js
 * Tells Tailwind which files to scan for class names so it can
 * generate only the CSS actually used (smaller production build).
 * ========================================================= */
module.exports = {
  content: [
    "./pages/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
