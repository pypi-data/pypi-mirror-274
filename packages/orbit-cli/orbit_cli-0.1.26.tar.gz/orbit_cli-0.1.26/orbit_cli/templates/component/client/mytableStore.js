import { defineStore } from 'pinia'

export const useMyTableStore = defineStore('mytableStore', {
    state: () => {
        return {
            model: 'mytable'
        }
    },
    actions: {
        sort (params) {},
        populate (label, callback=null) {
            const method = `api_${this.model}_get_ids`
            this.query({model: this.model, label: label, component: label, method: method},
                (response) => {
                    if (!response || !response.ok)
                        throw new Error(response ? response.error : `no query: ${method}`)
                    if (callback) callback(response)
                }
            )
            return this
        }
    },
    useOrmPlugin: true
})