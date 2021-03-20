import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.esm.browser.js'

new Vue({
    el: '#app',
    data: {
            table: [
                {"status": false, "name": "ToDo"},
                {"status": true, "name": "Done"},
            ],
            form_task: {'title': ''},
            form_file: {},
            categories: [],
            current_category: 1
    },
    methods: {
        async getData() {
            this.categories = await request('/category/all')
        },
        async createTask() {
            console.log(this.form_task)
            const req = {"title": this.form_task.title, 'id_category': this.current_category}
            this.last_added_task = await request('/task/', 'POST', req)
            await this.getData()
            this.form_task.title = ''
        },
        async deleteTask(id) {
            this.last_deleted_task = await request('/task/', 'DELETE', {"id": id})
            await this.getData()
        },
        async editStatusTask(task) {
            const data = {
                'id': task.id,
                'title': task.title,
                'status': !task.status,
                'category': task.category
            }
            this.last_edited_task = await request('/task/', 'PUT', data)
            await this.getData()
        },

        async openCategory(id) {
            this.current_category = id
            console.log(this.categories)
        },
        async createCategory(name) {
            const res = await request('/category/', 'POST', {"name": name})
            this.current_category = res.current_category
            await this.getData()

        },
        async deleteCategory(id) {
            this.last_deleted_category = await request('/category/', 'DELETE', {"id": id})
            if (this.last_deleted_category.id === this.current_category) {
                this.current_category = 1
            }
            await this.getData()
        },
        async editCategory(name) {
            this.last_edit_category = await request('/category/', 'PUT', {"name": name})
            await this.getData()
        },

        async downloadFile(task) {
            this.last_added_file = request('/file/download', 'GET', {"id_task": task.id})
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

async function request(url, method = 'GET', data = null, type= 'application/json') {
    try {
        const headers = {}
        let body;

        headers['Authorization'] = "Bearer " + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjE2MjQ5NTY5LCJqdGkiOiJiMzBmMmRiMC1jNjE0LTQ3NzgtODFhNC0zMjVkOWEwMDE0ZjIiLCJuYmYiOjE2MTYyNDk1NjksInR5cGUiOiJhY2Nlc3MiLCJzdWIiOjEsImNzcmYiOiI5ODljOGM1Ny02MzFhLTQ5YjEtOTJkYy1kOWRmZDIwNmM5NmMiLCJleHAiOjE2MTYyNTA0Njl9.hudpEoS5FqZj3Yk7eCXILlmrBrlNIv5OOi0HqBRpY7c'
        if (data) {
            headers['Content-type'] = type
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
