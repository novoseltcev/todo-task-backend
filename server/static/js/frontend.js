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
            current_category: 1,
            token_type: 'Bearer ',
            access_token: "",
            refresh_token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNjI4NDExOCwianRpIjoiMWUzN2ExOGQtNzdmNy00OGRlLWIyZDQtYjRjMDJmMmQ5YmIxIiwibmJmIjoxNjE2Mjg0MTE4LCJ0eXBlIjoicmVmcmVzaCIsInN1YiI6MSwiY3NyZiI6ImJlMzE4ZjExLWI4YzMtNGRjMi04ODJmLTE4M2JjNjYxNmExZiIsImV4cCI6MTYxNzU4MDExOH0.JL9hdPVdcGzKXJQa19p23-Fb9PpSV9XPrB6_JtBEpRg"
    },
    methods: {
        async request(url, method = 'GET', data = null, refresh=false) {
            try {
                const headers = {}
                let body
                if (!refresh) {
                    headers['Authorization'] = this.token_type + this.access_token
                } else {
                    headers['Authorization'] = this.token_type + this.refresh_token
                }

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
        },

        async getData() {
            const result = await this.request('/category/all')
            if (result.error) {
                const result_refresh = await this.request('/user/refresh', 'GET', null, true)
                if (result_refresh.access_token) {
                    this.access_token = result_refresh.access_token
                    this.categories =await this.request('/category/all')
                } else {
                    throw DOMException('aaaaaaa')
                }
            } else {
                this.categories = result
            }
        },
        async createTask() {
            console.log(this.form_task)
            const req = {"title": this.form_task.title, 'id_category': this.current_category}
            this.last_added_task = await this.request('/task/', 'POST', req)
            await this.getData()
            this.form_task.title = ''
        },
        async deleteTask(id) {
            this.last_deleted_task = await this.request('/task/', 'DELETE', {"id": id})
            await this.getData()
        },
        async editStatusTask(task) {
            const data = {
                'id': task.id,
                'title': task.title,
                'status': !task.status,
                'category': task.category
            }
            this.last_edited_task = await this.request('/task/', 'PUT', data)
            await this.getData()
        },

        async openCategory(id) {
            this.current_category = id
            console.log(this.categories)
        },
        async createCategory(name) {
            const res = await this.request('/category/', 'POST', {"name": name})
            this.current_category = res.current_category
            await this.getData()

        },
        async deleteCategory(id) {
            this.last_deleted_category = await this.request('/category/', 'DELETE', {"id": id})
            if (this.last_deleted_category.id === this.current_category) {
                this.current_category = 1
            }
            await this.getData()
        },
        async editCategory(name) {
            this.last_edit_category = await this.request('/category/', 'PUT', {"name": name})
            await this.getData()
        },

        downloadFile(file) {
            this.last_added_file = this.request('/file/download', 'POST', {"id": file.id})
        },
        async deleteFile(file) {
            this.last_deleted_file = await this.request('/file/', 'DELETE', {"id": file.id})
            await this.getData()
        },


    },
    created: function () {
        this.getData();
    },
})