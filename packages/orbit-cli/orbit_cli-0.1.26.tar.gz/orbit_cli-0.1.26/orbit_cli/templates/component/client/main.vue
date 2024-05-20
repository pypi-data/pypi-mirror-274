<template>
    <section class="content {{ project }}">
        <div class="html">
            <h1>Orbit Component "{{ project }}"</h1>
            <p>This is just a template to show the contents of 'mytable'</p>
            <table class="people-table">
                <tr>
                    <th v-for="f in ['name', 'height', 'mass', 'skin_color', 'eye_color', 'gender']">{{ "{{ f }}" }}</th>
                </tr>
                <tr v-for="id in mytable_ids" :key="id">
                    <td v-for="f in ['name', 'height', 'mass', 'skin_color', 'eye_color', 'gender']">
                        {{ "{{ mytable_data.get(id)[f] }}" }}
                    </td>
                </tr>
            </table>
        </div>
    </section>
</template>

<script setup>
import { defineComponent, ref, watch, computed, inject, onMounted } from 'vue';
import { defineStore } from 'pinia';
import { OrbitComponentMixin } from '@/../node_modules/orbit-component-base';
import { useMyTableStore } from '@/stores/mytableStore.js';
import pkg from '../package.json';

const plugin        = inject('$orbitPlugin')
const socket        = ref({connected:false})
const mytableStore  = useMyTableStore()
const active        = computed(() => socket.value.connected)
const mytable_data  = computed(() => mytableStore.data)
const mytable_ids   = computed(() => mytableStore.ids(root.value))
const root          = computed(() => opt.router.currentRoute.value.meta.root)

onMounted(async () => {
    await plugin (opt, namespace, socket);
})

watch (active, (curr, last) => {
    if (curr && !last) {
        mytableStore.init(app, root.value, socket.value).populate(root.value)
    }
})
</script>

<script>
const namespace = 'mycomp'
const mixin = OrbitComponentMixin(namespace, defineStore)
const opt = ref(null)
const app = ref(null)

export default defineComponent({
    name: namespace,
    install (vue, options) {
        mixin.install (vue, options, this, app, opt)
    },
    bootstrap () {
        return mixin.bootstrap (pkg.version)
    },
})
</script>


<style scoped>
section.content.{{ project }} {
    flex: 1;
    border-top: 1px solid #bbb;
    border-left: 1px solid #bbb;
    border-top-left-radius: 10px;
    background-color: white;
    height: 1px;
}
section.content.{{ project }} div.html {
    display: flex;
    flex-direction: column;
    height: 100%;
    margin-left: 1em;
    margin-top: 0.5em;
    font-size: 1.1em;
    overflow-y: auto;
    padding-bottom: 2em;
}
section.content.{{ project }} .people-table {
    border: 2px solid cyan;
    margin-right: 1em;
    padding: 1em;
}
section.content.{{ project }} .people-table tr th {
    background-color: #333;
    color: white;
    font-weight: 600;
}
section.content.{{ project }} .people-table tr th,section.content.{{ project }} .people-table tr td {
    padding-left: 1em;
    padding-right: 1em;
}
</style>