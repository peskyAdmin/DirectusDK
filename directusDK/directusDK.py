import time
import requests
from slugify import slugify

MANY_TO_MANY_TEMPLATE = {
        "create": [],
        "update": [],
        "delete": []
    }


class DirectusDK:
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
        :param folder_names: list of parent folder names to find all leaf folders
        :param force: Force API update
        :return: list of leaf folder objects
        """
        if force:
            self.get_all_folders()

        leaf_folder_ids = []
        top_parent_ids = []
        for folder in self.folders:
            if folder['name'] in folder_names:
                top_parent_ids.append(folder['id'])

        leaf_folder_ids = list(self.find_leaf_folders(top_parent_ids))

        leaf_folder_objects = []
        for folder in self.folders:
            if folder['id'] in leaf_folder_ids:
                leaf_folder_objects.append(folder)

        return leaf_folder_objects

    def find_files_in_folders(self, folder_ids):
        files = []
        for file in self.files:
            if file['folder'] in folder_ids:
                files.append(file)
        return files

    def get_all_folders(self):
        # self.folders = _merge_dicts(self._api_get('/folders?limit=-1'))
        items = []
        page = 1
        print(f"Getting all folders 100 at a time")
        while True:
            print(f'Getting page {page}')
            response = self._api_get(f'/folders/?page={page}')
            # data = response.get('data', [])
            if not response:
                break
            items.extend(response)
            page += 1
        print(f'Got all {len(items)} folders')

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
        return self._api_patch(endpoint=f'/files/{file_id}', json=attributes)

    def get_all_items(self, collection):
        items = []
        page = 1
        print(f"Getting all items 100 at a time")
        while True:
            print(f'Getting page {page}')
            response = self._api_get(f'/items/{collection}?page={page}')
            # data = response.get('data', [])
            if not response:
                break
            items.extend(response)
            page += 1
        print(f'Got all {len(items)} items')
        return items

    def get_item(self, collection, item_id):
        return self._api_get(f'/items/{collection}/{item_id}')

    def update_item(self, collection, item_id, attributes):
        return self._api_patch(f'/items/{collection}/{item_id}', json=attributes)

    def create_item(self, collection, attributes):
        return self._api_post(endpoint=f'/items/{collection}', json=attributes)

    def get_all_collections(self):
        self.collections = self._api_get(f'/collections')
        return self.collections

    def get_collection(self, collection):
        return self._api_get(f'/collections/{collection}')

    def delete_collection(self, collection):
        return self._api_delete(f'/collections/{collection}')

    def update_collection(self, collection, attributes):
        return self._api_patch(f'/collections/{collection}', json=attributes)

    def create_collection(self, collection, attributes):
        """
            {"collection": "collection_name",
             "field": {"sub_field": "value"}}


        :param collection:
        :param attributes:
        :return:
        """
        return self._api_post(f'/collection', json=attributes)

    def get_fields(self):
        return self._api_get('/fields')

    def get_fields_in_collection(self, collection):
        return self._api_get(f'/fields/{collection}')

    def clone_collection(self, old_collection, new_collection, override = None):
        """
        pass dictionary to override, rename fields
        dict = {
            'id': 'group_id',
            'status': 'status_new'
        }
        """

        fields = self.get_fields_in_collection(old_collection)

        for field in fields:
            if field['field'] == 'id':
                id_field = field

        self.create_collection(new_collection)

        # TODO: handle id creation
        for field in fields:
            if field['field'] != 'id':
                #TODO: implement override
                del field['meta']['id']
                del field['meta']['collection']
                del field['meta']['field']

                data = {
                    'field': field['field'],
                    'type': field['type'],
                    'meta': field['meta'],
                    'schema': field['schema']
                }

                self.create_field(new_collection, data)

    def get_field(self, collection, field):
        return self._api_get(f'/fields/{collection}/{field}')

    def create_field_dropdown(self, collection, field_name, dropdown_options, type="string"):
        """
        :param collection: collection to create field
        :param field_name: name of field to create
        :param dropdown_options: a list of choice objects ie
                        [{
                            "text": "test1",
                            "value": "test1"
                        }]
        :return:
        """
        field_data = {"field": field_name,
                      "type": type,
                      "schema": {},
                      "meta": {"interface": "select-dropdown",
                               "special": None,
                               "options": {"choices": dropdown_options}},
                      "collection": collection}

        return self.create_field(collection=collection, field_data=field_data)

    def create_field(self, collection, field_data):
        """
        {"field": "field_key",
	     "type": "value_type",
	     "field_field": {"field_sub_field": "value_1"}}

        :param collection:
        :param field_data:
        :return:
        """
        return self._api_post(endpoint=f'/fields/{collection}', json=field_data)

    def update_field(self, collection, field, field_data):
        """
        {"field": {"sub_field": "value_1"}}

        :param collection:
        :param field:
        :param field_data:
        :return:
        """
        return self._api_patch(endpoint=f'/fields/{collection}/{field}', json=field_data)

    def delete_field(self, collection, field):
        return self._api_delete(endpoint=f'/fields/{collection}/{field}')

    def _api_get(self, endpoint):
        return self._send_request_handle_response(endpoint=endpoint, 
                                                  headers=self.auth_header, 
                                                  method='get')


    def _api_patch(self, endpoint, json):
        return self._send_request_handle_response(endpoint=endpoint,
                                                  headers=self.auth_header,
                                                  method='patch',
                                                  json=json)

    def _api_post(self, endpoint, json):
        return self._send_request_handle_response(endpoint=endpoint,
                                                    headers=self.auth_header,
                                                    method='post',
                                                    json=json)

    def _api_delete(self, endpoint):
        return self._send_request_handle_response(endpoint=endpoint,
                                                  headers=self.auth_header,
                                                  method='delete')

    def _send_request_handle_response(self, endpoint, headers, method, json=None):
        max_retries = 5
        num_tries = 1
        url = self.url + endpoint
        res = requests.request(method=method, url=url, headers=headers, json=json)
        if res.status_code == 502 or res.status_code == 503 or res.status_code == 500:
            print(f'ERROR: Bad Response {res}')
            print(f'ERROR: Endpoint: {url}')
            print(f'ERROR: Retrying {max_retries} more times')
            try: 
                data = res.json()
                print(f'ERROR: Data: {data}')
            except Exception as e:
                print(f'ERROR: No Data {e}')
            for i in range(max_retries):
                res = requests.request(method=method, url=url, headers=headers, json=json)
                if res.status_code == 200:
                    data = res.json()
                    return data['data']
                elif num_tries == max_retries:
                    raise Exception(f'ERROR: Bad Response {res}')
                else:
                    num_tries += 1
                    print(f'ERROR: Bad Response {res}')
                    print(f'Waiting 10 seconds')
                    time.sleep(10)
        elif not res.status_code == 200:
            print(f'ERROR: Bad Response {res}')
            print(res.content)
            print(f'ERROR: Data: {data}')
            print(f'ERROR: Endpoint: {endpoint}')
            return False
        else:
            data = res.json()
            return data['data'] 

def _merge_dicts(list_of_dicts):
    merged_dict = {d["id"]: {k: v for k, v in d.items() if k != "id"} for d in list_of_dicts}
    return merged_dict


