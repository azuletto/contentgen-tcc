module.exports = {
  content: ["./index.html", "./src/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
  corePlugins: {
    preflight: false, // Evita conflitos com Material-UI
  },
};
