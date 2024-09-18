import { createApp, defineAsyncComponent } from 'vue';
import { createRouter, createWebHashHistory } from 'vue-router';
import vClickOutside from "click-outside-vue3";

import App from './components/App.vue';

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            redirect: '/messages',
        },
        {
            name: "about",
            path: '/about',
            component: defineAsyncComponent(() => import("./components/about/AboutPage.vue")),
        },
        {
            name: "interfaces",
            path: '/interfaces',
            component: defineAsyncComponent(() => import("./components/interfaces/InterfacesPage.vue")),
        },
        {
            name: "interfaces.add",
            path: '/interfaces/add',
            component: defineAsyncComponent(() => import("./components/interfaces/AddInterfacePage.vue")),
        },
        {
            name: "interfaces.edit",
            path: '/interfaces/edit',
            component: defineAsyncComponent(() => import("./components/interfaces/AddInterfacePage.vue")),
            props: {
                interface_name: String,
            },
        },
        {
            name: "messages",
            path: '/messages',
            component: defineAsyncComponent(() => import("./components/messages/MessagesPage.vue")),
        },
        {
            name: "network-visualiser",
            path: '/network-visualiser',
            component: defineAsyncComponent(() => import("./components/network-visualiser/NetworkVisualiserPage.vue")),
        },
        {
            name: "nomadnetwork",
            path: '/nomadnetwork',
            component: defineAsyncComponent(() => import("./components/nomadnetwork/NomadNetworkPage.vue")),
        },
        {
            name: "propagation-nodes",
            path: '/propagation-nodes',
            component: defineAsyncComponent(() => import("./components/propagation-nodes/PropagationNodesPage.vue")),
        },
        {
            name: "settings",
            path: '/settings',
            component: defineAsyncComponent(() => import("./components/settings/SettingsPage.vue")),
        },
    ],
})

createApp(App)
    .use(router)
    .use(vClickOutside)
    .mount('#app');
