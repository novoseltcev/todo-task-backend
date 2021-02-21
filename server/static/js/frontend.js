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
                ],
            current_category: 1,
        },
    methods: {
        async getData() {
            this.categories = await request('/category/all', 'GET')
            console.log(this.categories)
        },
        async createTask() {
            const {...cur_task} = this.form_task
            this.last_added_task = await request('/task/', 'POST', {"title": {...cur_task}.title})
            await this.getData()
            this.form_task.title = ''
        },
        async deleteTask(id) {
            this.last_deleted_task = await request('/task/', 'DELETE', {"id": id})
            await this.getData()
        },
        async editStatusTask(id) {
            this.last_edited_task = await request('/task/status', 'PUT', {"id": id})
            await this.getData()
        },

        async openCategory(id) {
            const res = await request('/category/open', 'POST', {"id": id})
            this.current_category = res.current_category
            console.log(this.current_category)
        },
        async createCategory(name) {
            const res = await request('/category/', 'POST', {"name": name})
            this.current_category = res.current_category
            await this.getData()

        },
        async deleteCategory(id) {
            this.last_deleted_category = await request('/category/', 'DELETE', {"id": id})
            await this.getData()
        },
        async editCategory(name) {
            this.last_edit_category = await request('/category/', 'PUT', {"name": name})
            await this.getData()
        },

        async downloadFile(id) {
            this.last_added_file = await request('/file/download', 'GET', {"id": id})
            await this.getData()
        },
        async createFile(file) {
            this.last_added_file = await request('/file/', 'POST', {"file": file})
            await this.getData()
        },
        async deleteFile(id) {
            this.last_deleted_file = await request('/file/', 'DELETE', {"id": id})
            await this.getData()
        },
    },
    created: function () {
     this.getData();
    },
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
