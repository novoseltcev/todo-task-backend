from server.istorage import IStorage


class ServerOperationOnDB:
    storage = IStorage

    def init_storage(self, storage: IStorage):
        self.storage = storage

    def create_task(self, json: dict):
        if 'title' in json:
            task_title = json['title']
            self.storage.append_task(task_title)
            return True
        return False

    def create_category(self, json: dict):
        if 'category' in json and json.get('operation') == 'create':
            task_category = json['category']
            self.storage.append_category(task_category)
            return True
        return False

    def open_category(self, json: dict):
        if 'category' in json and json.get('operation') == 'open':
            self.storage.current_category = json['category']
            return True
        return False

    def change_task_status(self, json: dict):
        if 'id' in json and 'category' not in json:
            task_id = json['id']
            self.storage.update_task_status(task_id)
            return True
        return False

    def change_task_category(self, json: dict):
        if 'id' in json and 'category' in json:
            task_id = json['id']
            category_name = json['category']
            self.storage.update_task_category(task_id, category_name)
            return True
        return False

    def change_category_name(self, json: dict):
        if 'destination_category' in json and 'source_category' in json:
            destination = json['destination_category']
            source = json['source_category']
            self.storage.rename_category(destination, source)
            return True
        return False

    def delete_task(self, json: dict):
        if 'id' in json:
            task_id = json['id']
            self.storage.remove_task(task_id)
            return True
        return False

    def delete_category(self, json: dict):
        if 'category' in json:
            category_name = json['category']
            self.storage.remove_category(category_name)
            return True
        return False

    def get_data(self, json: dict):
        """"fghj"""
