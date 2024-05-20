{% for font in fonts %}import "{{font}}";
{% endfor %}
import { createApp, reactive } from 'vue'
import { createPinia } from 'pinia';
import { createRouter, createWebHashHistory } from 'vue-router'
import { OrbitConnection, BaseClass } from '@/../node_modules/orbit-component-base'
{% for (name, component) in components %}import { menu as {{ name }} } from '{{ component }}';
{% endfor %}
import App from './App.vue'
import metadata from '@/../package.json';
import '@/assets/main.css';

const router = createRouter({ history: createWebHashHistory(), routes: [] })
const pinia = createPinia()
const app = createApp(App)
app.metadata = metadata
app.metadata.components = new Map()

pinia.use(BaseClass)
app.use(OrbitConnection)

const menu = reactive([])
app.provide('$menu', menu)
{% for (name, _) in components %}{{ name }}(app, router, menu);
{% endfor %}
app.use(pinia)
app.use(router)
app.mount('#app')
