import path from "path";
import vue from '@vitejs/plugin-vue';
import vuetify from 'vite-plugin-vuetify';
import { VitePWA } from 'vite-plugin-pwa'


export default {
  plugins: [
    vue(),
    vuetify(),
    VitePWA({
        workbox: {
            maximumFileSizeToCacheInBytes: 3000000,
      },
      registerType: 'autoUpdate', // Automatically update the service worker when a new version is available
      manifest: {
        name: 'Reticulum MeshChat',
        short_name: 'MeshChat',
        description: 'A simple mesh network communications app powered by the Reticulum Network Stack.',
        theme_color: '#ffffff',
        icons: [
          {
            src: '/logo/logo-192.png',  // Reference the icon in the public folder
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: '/logo/icon-512.png',  // Larger icon for better resolution
            sizes: '512x512',
            type: 'image/png',
          },
        ],
      },
    }),
  ],



    // vite app is loaded from /src/frontend
    root: path.join(__dirname, "src", "frontend"),

    build: {

        // we want to compile vite app to /public which is bundled and served by the python executable
        outDir: path.join(__dirname, "public"),
        emptyOutDir: true,

        rollupOptions: {
            input: {

                // we want to use /src/frontend/index.html as the entrypoint for this vite app
                app: path.join(__dirname, "src", "frontend", "index.html"),

                // we want to use /src/frontend/call.html as the entrypoint for the phone call app
                call: path.join(__dirname, "src", "frontend", "call.html"),

            },
        },
    },

}

