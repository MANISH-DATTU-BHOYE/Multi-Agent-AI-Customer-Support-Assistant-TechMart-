// =========================================================
// frontend/pages/_app.jsx
// -----------------------------------------------------------
// Next.js root component. Imports global styles once so every
// page/component gets Tailwind's utility classes.
// =========================================================

import "../styles/globals.css";

export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />;
}
