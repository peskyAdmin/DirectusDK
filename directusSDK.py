import requests


class DirectusSDK:
    def __init__(self, url, api_token, force=False):
        self.url = url
        self.auth_header = {'Authorization': f'Bearer {api_token}'}

        if force:
            self.folders = self.get_all_folders()
            self.files = self.get_all_files()
            self.collections = self.get_all_collections()
        else:
            self.folders = None
            self.files = None
            self.collections = None

        print('Finished Init')

    def find_leaf_folders(self, list_folder_ids, force=False):
        """
        Recursive function to find all bottom level folders in provided list of folder ids

        :param list_folder_ids: list of parent folder ids
        :param force: Force API update
        :return:
        """
        if force:
            self.get_all_folders()

        leaf_folders = set(list_folder_ids)                                 # Set folders to recursively update
        sub_folders = set()                                                 # Set of sub folders
        parent_folders = set()                                              # Set of folder IDs that contain sub folders

        for folder in self.folders:                                         # Iterate through all folders
            if folder['parent'] in list_folder_ids:                         # If folder has parent in current set
                parent_folders.add(folder['parent'])                        # Add current parent folder to parent set
                sub_folders.add(folder['id'])                               # Add new sub folder to sub folder set

        leaf_folders = leaf_folders.difference(parent_folders)              # Remove parent folders from current set
        leaf_folders = leaf_folders.union(sub_folders)                      # Add sub folders to current set

        if not list_folder_ids == leaf_folders:                             # if new sub folders were found
            leaf_folders = self.find_leaf_folders(leaf_folders)             # Repeat

        return leaf_folders                                                 # Return set of sub folders

    def find_leaf_folders_by_name(self, folder_names, force=False):
        """
        :param folder_name: list of parent folder names to find all leaf folders
        :param force: Force API update
        :return: list of leaf folder ids
        """
        if force:
            self.get_all_folders()

        top_parent_ids = []
        for folder in self.folders:
            if folder['name'] in folder_names:
                top_parent_ids.append(folder['id'])
                leaf_folders = self.find_leaf_folders(top_parent_ids)
                return leaf_folders

    def find_files_in_folders(self, folder_ids):
        files = []
        # for file in self.files.keys():
        for file in self.files:
            if file['folder'] in folder_ids:
                files.append(file)
        return files

    def find_files_in_folders_new(self, folder_ids):
        files = []
        # for file, datain self.files.items():
        for file in self.files:
            if file['folder'] in folder_ids:
                files.append(file)
        return files

    def get_all_folders(self):
        # self.folders = _merge_dicts(self._api_get('/folders?limit=-1'))
        self.folders = self._api_get('/folders?limit=-1')
        return self.folders

    def get_folder(self, folder_id):
        return self._api_get(f'/folders/{folder_id}')

    def get_all_files(self):
        # self.files = _merge_dicts(self._api_get('/files?limit=-1'))
        self.files = self._api_get('/files?limit=-1')
        return self.files

    def get_file(self, file_id):
        return self._api_get(f'/files/{file_id}')

    def update_file(self, attributes, file_id):
        self._api_patch(endpoint=f'/files/{file_id}', json=attributes)

    def get_all_items(self, collection):
        # return _merge_dicts(self._api_get(f'/items/{collection}?limit=-1'))
        return self._api_get(f'/items/{collection}?limit=-1')

    def get_item(self, collection, item_id):
        return self._api_get(f'/items/{collection}/{item_id}')

    def update_item(self, collection, item_id, attributes):
        self._api_patch(f'/items/{collection}/{item_id}', json=attributes)

    def get_all_collections(self):
        self.collections = self._api_get(f'/collections')
        return self.collections

    def get_collection(self, collection):
        return self._api_get(f'/collections/{collection}')

    def delete_collection(self, collection):
        self._api_delete(f'/collections/{collection}')

    def update_collection(self, collection, attributes):
        self._api_patch(f'/collections/{collection}', json=attributes)

    def create_collection(self, collection, attributes):
        """
            {"collection": "collection_name",
             "field": {"sub_field": "value"}}


        :param collection:
        :param attributes:
        :return:
        """
        self._api_post(f'/collection', json=attributes)

    def get_fields(self):
        return self._api_get('/fields')

    def get_fields_in_collection(self, collection):
        return self._api_get(f'/fields/{collection}')

    def get_field(self, collection, field):
        return self._api_get(f'/fields/{collection}/{field}')

    def create_field(self, collection, field_data):
        """
        {"field": "field_key",
	     "type": "value_type",
	     "field_field": {"field_sub_field": "value_1"}}

        :param collection:
        :param field_data:
        :return:
        """
        self._api_post(endpoint=f'/fields/{collection}', json=field_data)

    def update_field(self, collection, field, field_data):
        """
        {"field": {"sub_field": "value_1"}}

        :param collection:
        :param field:
        :param field_data:
        :return:
        """
        self._api_patch(endpoint=f'/fields/{collection}/{field}', json=field_data)

    def delete_field(self, collection, field):
        self._api_delete(endpoint=f'/fields/{collection}/{field}')

    def _api_get(self, endpoint):
        res = requests.get(url=self.url + endpoint, headers=self.auth_header)
        data = _handle_api_response(res, endpoint)

        return data

    def _api_patch(self, endpoint, json):
        res = requests.patch(url=self.url + endpoint, headers=self.auth_header, json=json)
        data = _handle_api_response(res, endpoint)

        return data

    def _api_post(self, endpoint, json):
        res = requests.post(url=self.url + endpoint, headers=self.auth_header, json=json)
        data = _handle_api_response(res, endpoint)

    def _api_delete(self, endpoint):
        res = requests.delete(url=self.url + endpoint)

def _handle_api_response(res, endpoint):
    data = res.json()
    if not res.status_code == 200:
        print(f'ERROR: Bad Response {res}')
        print(f'ERROR: Data: {data}')
        print(f'ERROR: Endpoint: {endpoint}')
    return data['data']


def _merge_dicts(list_of_dicts):
    merged_dict = {d["id"]: {k: v for k, v in d.items() if k != "id"} for d in list_of_dicts}
    return merged_dict


