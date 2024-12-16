import axios from 'axios';
import {createApp} from 'vue';
import "./style.css";
import CallPage from "./components/call/CallPage.vue";

// provide axios globally
window.axios = axios;

createApp(CallPage)
    .mount('#app');
