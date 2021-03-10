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
            categories: [
                ],
            current_category: 1,
            auth_token: ""
    },
    methods: {
        async getData() {
            this.categories = await request('/category/all')
        },
        async createTask() {
            console.log(this.form_task)
            const req = {"title": this.form_task.title, 'category_id': this.current_category}
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

        downloadFile(task) {
            this.last_added_file = request('/file/download', 'GET', {"task_id": task.id})
            // this.getData()
        },
        async createFile(id) {
            this.last_added_file = await request('/file/', 'POST', {"id": id, 'file': file}, 'multipart/form-data')
            await this.getData()
        },
        async deleteFile(id) {
            this.last_deleted_file = await request('/file/', 'DELETE', {"id": id})
            await this.getData()
        },

        async submitFile(id) {
            this.last_added_file = await request('/file/', 'POST', this.form_file, 'multipart/form-data')
        },

        submitFile2(event) {
            this.form_file = event.target.files
        }

    },
    created: function () {
        this.getData();
    },
})

async function request(url, method = 'GET', data = null, type= 'application/json') {
    try {
        const headers = {}
        let body

        if (!this.auth_token) {
            headers['Authorization'] = "Bearer " + this.auth_token
        }

        if (data) {
            headers['Content-type'] = type
            if (type !== 'application/json') {
                body = new FormData()
                body.append('file', data)
            } else {
                body = JSON.stringify(data)
            }
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
