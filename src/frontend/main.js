import { createApp } from 'vue';
import { createRouter, createWebHashHistory } from 'vue-router';

import App from './components/App.vue';
import AboutPage from "./components/about/AboutPage.vue";
import SettingsPage from "./components/settings/SettingsPage.vue";
import NetworkVisualiserPage from "./components/network/NetworkVisualiserPage.vue";
import InterfacesPage from "./components/interfaces/InterfacesPage.vue";
import NomadNetworkPage from "./components/nomadnetwork/NomadNetworkPage.vue";
import MessagesPage from "./components/messages/MessagesPage.vue";
import AddInterfacePage from "./components/interfaces/AddInterfacePage.vue";

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        { path: '/', redirect: '/messages' },
        { path: '/about', name: "about", component: AboutPage },
        { path: '/messages', name: "messages", component: MessagesPage },
        { path: '/nomadnetwork', name: "nomadnetwork", component: NomadNetworkPage },
        { path: '/settings', name: "settings", component: SettingsPage },
        { path: '/interfaces', name: "interfaces", component: InterfacesPage },
        { path: '/interfaces/add', name: "interfaces.add", component: AddInterfacePage },
        { path: '/interfaces/edit', name: "interfaces.edit", component: AddInterfacePage, props: { interface_name: String } },
        { path: '/network-visualiser', name: "network-visualiser", component: NetworkVisualiserPage },
    ],
})

createApp(App)
    .use(router)
    .mount('#app');
