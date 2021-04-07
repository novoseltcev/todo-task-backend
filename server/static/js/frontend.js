import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.esm.browser.js'

new Vue({
    el: '#app',
    data: {
            table: [
                {status: false, name: "ToDo"},
                {status: true, name: "Done"},
            ],
            form_task: {title: ''},
            form_login: {username: '', password: ''},
            form_file: {},
            categories: [],
            current_category: 1,
            tokens: {type: 'Bearer ',
                access_token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjE3ODAwNjk5LCJqdGkiOiIzODBkNDJjZC0zMjc1LTRmNWMtYTY5MS03OTc0ZTcxZWEyMDYiLCJuYmYiOjE2MTc4MDA2OTksInR5cGUiOiJhY2Nlc3MiLCJzdWIiOjEsImNzcmYiOiIyODZmZGIyYy1mN2M2LTRkYmUtODFhNy05Y2Y3YzY5NGJmM2UiLCJleHAiOjE2MTc4MDE1OTksInJvbGUiOiJvd25lciJ9.y7sSivjfBjeBP4CVAI9lRiHCulQkWmx2QAqoH4HbRwM",
                refresh_token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNzY2NDgyNCwianRpIjoiMjIwMDJmNGYtNDlhZC00ZWU0LWFiM2ItNWEzYmIzYmUzNzU0IiwibmJmIjoxNjE3NjY0ODI0LCJ0eXBlIjoicmVmcmVzaCIsInN1YiI6MSwiY3NyZiI6IjQ5MWFiMDgzLWQ1ODUtNDA4Yy04OWQxLWFmZWJiNTI2YWIzYyIsImV4cCI6MTYxODk2MDgyNH0.owJD2nVQ9TNJyy8kC7mAnWgEdct0Qcew9jraCTwT6hc"
            },
            current_user: {admin: true, username: "st-a-novoseltcev"}
    },
    methods: {
        async request(url, method = 'GET', data = null, refresh=false) {
            try {
                const headers = {}
                let body
                if (!refresh) {
                    headers['Authorization'] = this.tokens.type + this.tokens.access_token
                } else {
                    headers['Authorization'] = this.tokens.type + this.tokens.refresh_token
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
            const result = await this.request('/categories/')
            if (result.expired_error) {
                const result_refresh = await this.request('/user/refresh', 'GET', null, true)
                if (result_refresh.access_token) {
                    this.tokens.access_token = result_refresh.access_token
                    this.categories =await this.request('/categories/')
                } else {
                    throw new DOMException('')
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

        userLogin() {
            const req = {"login": this.form_login.username, 'password': this.form_login.password}
            this.token = this.request('/login', 'POST', req);
            this.form_login.username = ''
            this.form_login.password = ''
            window.location = '/'
        }
    },
    created: function () {
        this.getData();
    },
})