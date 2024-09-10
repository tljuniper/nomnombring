import './assets/main.css'
import axios from "axios";

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

fetch("/config.json")
    .then((response) => response.json())
    .then((config) => {
        axios.defaults.baseURL = config.BACKEND_URL;
        // FINALLY, mount the app
        app.mount("#app")
    })
