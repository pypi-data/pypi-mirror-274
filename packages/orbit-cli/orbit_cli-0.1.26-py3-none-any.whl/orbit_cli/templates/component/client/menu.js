import {{ project }} from '@/../node_modules/orbit-component-{{ project }}'
import QuestionMarkOutlined from '@vicons/material/QuestionMarkOutlined.js'
import { shallowRef } from 'vue'

export function menu (app, router, menu) {
    const IconAPI = shallowRef(QuestionMarkOutlined)
    app.use({{ project }}, {
        router: router,
        menu: menu,
        root: '{{ project }}',
        buttons: [
            {name: '{{ project }}', text: '{{ project }}'  , component: {{ project }} , icon: IconAPI , pri: 1, path: '/{{ project }}', meta: {root: '{{ project }}', host: location.host}},
        ]
    })
}