import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.esm.browser.js'

new Vue({
    el: '#app',
    data: {
            table: [
                {"id": 0, "name": "ToDo"},
                {"id": 1, "name": "Done"},
            ],
            form_task: {
                'title': ''
            },
            categories: [
                {'id': 1, 'name': "All", 'tasks': [{'id': 1, 'title': "HW", 'status': 1, 'files':[]}]}
                ],
            current_category: 1,
        },
    methods: {
        async createTask() {
            const {...cur_task} = this.form_task
            this.categories = await request('/task/', 'POST', {"title": {...cur_task}.title})
            this.form_task.title = ''
        },
        async openCategory(id) {
            const res = await request('/category/current', 'POST', {"id": id})
            this.categories = res.categories
            this.current_category = res.current_category
            console.log(this.categories)
            console.log(this.current_category)
        },
        async deleteTask(id) {
            this.categories = await request('/task/', 'DELETE', {"id": id})
            console.log(this.categories)
        },
        async editStatusTask(id) {
            this.categories = await request('/task/status', 'PUT', {"id": id})
            console.log(this.categories)
        },
        async createFile(task) {
            this.categories = await request('/file/', 'POST', {"task": task})
            console.log(this.categories)
        },
        async deleteFile(id) {
            this.categories = await request('/file/', 'DELETE', {"id": id})
            console.log(this.categories)
        },
    }
})

async function request(url, method = 'GET', data = null) {
    try {
        const headers = {}
        let body

        if (data) {
            headers['Content-type'] = 'application/json'
            body = JSON.stringify(data)
            console.log(data)
        }

        const response = await fetch(url, {
            method: method,
            headers: headers,
            body: body
        })
        return await response.json( )
    } catch (e) {
        console.warn('Error', e.message)
    }
}
