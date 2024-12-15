import formsPlugin from '@tailwindcss/forms';

/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'selector',
    content: [
        "./src/frontend/index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx,html}",
    ],
    theme: {
        extend: {},
    },
    plugins: [
        formsPlugin,
    ],
}

