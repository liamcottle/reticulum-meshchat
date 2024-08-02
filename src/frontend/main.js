import { createApp } from 'vue';
import { createRouter, createWebHashHistory } from 'vue-router';

import App from './components/App.vue';
import AboutPage from "./components/about/AboutPage.vue";
import SettingsPage from "./components/settings/SettingsPage.vue";
import NetworkVisualiserPage from "./components/network/NetworkVisualiserPage.vue";

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        { path: '/' },
        { path: '/about', name: "about", component: AboutPage },
        { path: '/settings', name: "settings", component: SettingsPage },
        { path: '/network-visualiser', name: "network-visualiser", component: NetworkVisualiserPage },
    ],
})

createApp(App)
    .use(router)
    .mount('#app');
