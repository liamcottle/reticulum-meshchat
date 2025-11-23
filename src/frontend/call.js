import axios from 'axios';
import {createApp} from 'vue';
import "./style.css";
import TelephonePage from "./components/telephone/TelephonePage.vue";

// provide axios globally
window.axios = axios;

createApp(TelephonePage)
    .mount('#app');
