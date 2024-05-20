<template>
    <section class="content {{ project }}">
        <div class="html">
            <h1>Orbit Component "{{ project }}"</h1>
            <p>This is just a template to show the contents of 'mytable'</p>
            <table class="people-table">
                <tr v-for="id in mytable_ids" :key="id">
                    <td v-for="f in ['name', 'height', 'mass', 'skin_color', 'eye_color', 'gender']">
                        {{  '{{ mytable_data.get(id)[f] }}' }}
                    </td>
                </tr>
            </table>
        </div>
    </section>
</template>

<script setup>
import { getCurrentInstance, defineComponent, ref, watch, computed, inject, onMounted } from 'vue'
import { useMyTableStore } from '@/stores/mytableStore.js';
const namespace     = '{{ project }}'
const socket        = ref(null)
const active        = ref(false)
const plugin        = inject('$orbitPlugin')
const meta          = ref(null)
const mytableStore  = useMyTableStore()
const mytable_ids   = computed(() => { return meta.value ? mytableStore.ids(meta.value.root) : [] })
const mytable_data  = computed(() => { return mytableStore.data})

onMounted(async () => {
    await router.isReady;
    meta.value = router.currentRoute.value.meta
    plugin (meta.value.root, namespace, active, socket, meta.value.host);
})
watch (active, (newState, oldState) => {
    if (newState && !oldState) mytableStore.init(
        getCurrentInstance(),
        meta.value.root,
        socket.value
    ).populate(meta.value.root)
})
</script>

<script>
let router = null

export default defineComponent({
    name: '{{ project }}',
    install (app, options) {
        app.component('{{ project }}', this);
        (options.buttons||[]).forEach((button) => {
            options.router.addRoute(button)
            options.menu.push(button)
        })
        router = options.router
    }
})
</script>

<style>
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
</style>
