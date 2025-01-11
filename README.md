# DirectusDK - Directus Python Development Kit

![DirectusDK Logo](images/logo.jpg)

## Overview

**DirectusDK** is a Python wrapper for interacting with the Directus API. This library simplifies the process of managing collections, items, files, and folders within a Directus project through a set of Python classes and methods.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Methods](#api-methods)
  - [Initialization](#initialization)
  - [Folder Management](#folder-management)
  - [File Management](#file-management)
  - [Item Management](#item-management)
  - [Collection Management](#collection-management)
  - [Field Management](#field-management)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the DirectusDK, you can use pip:


This SDK is not currently on PYPI therefore you have to clone and install manually
```bash
git clone https://github.com/peskyAdmin/DirectusDK
cd directusdk
python setup.py install
```

if you want to write scpripts and develop on DirectusDK at the same time then clone the project and inside the project run:

```bash
pip install -e .
```

This will allow you to make changes and have them immedieatly take affect in your environment.

## Configuration
Before using DirectusDK, you need to set up your Directus project and obtain an API token:

Directus URL: The base URL of your Directus instance.
API Token: Generated from the Directus Admin panel under User Settings.

Here's how you would initialize the class:


```python
from directusDK.directusDK import DirectusDK

directus = DirectusDK(url='https://your-directus-url.com', api_token='your-api-token')
```

Usage
Basic Example
```python
# Example of fetching all items
items = directus.get_all_items(collection='collection_name')
```

## API Methods

### Initialization

- **`init(url, api_token, force=False)`**: Initializes the DirectusDK instance.
  - **`url`**: The base URL for your Directus instance.
  - **`api_token`**: Your authentication token.
  - **`force`**: If True, it will refresh all data from the server during initialization.
### Folder Management

- **`find_leaf_folders(list_folder_ids, force=False)`**: Finds all bottom-level folders from a list of parent folder IDs.
- **`find_leaf_folders_by_name(folder_names, force=False)`**: Finds leaf folders by their names.
- **`get_all_folders()`**: Retrieves all folders from Directus.
- **`get_folder(folder_id)`**: Gets details of a specific folder.

### File Management

- **`get_all_files()`**: Retrieves all files.
- **`get_file(file_id)`**: Gets details of a specific file.
- **`update_file(attributes, file_id)`**: Updates file attributes.

### Item Management

- **`get_all_items(collection)`**: Retrieves all items from a collection.
- **`get_item(collection, item_id)`**: Gets a specific item from a collection.
- **`update_item(collection, item_id, attributes)`**: Updates an item.
- **`create_item(collection, attributes)`**: Creates a new item in the specified collection.

### Collection Management

- **`get_all_collections()`**: Fetches all collections.
- **`get_collection(collection)`**: Gets details of a specific collection.
- **`delete_collection(collection)`**: Deletes a collection.
- **`update_collection(collection, attributes)`**: Updates collection settings.
- **`create_collection(collection, attributes)`**: Creates a new collection.

### Field Management

- **`get_fields()`**: Retrieves all fields across collections.
- **`get_fields_in_collection(collection)`**: Gets fields for a specific collection.
- **`clone_collection(old_collection, new_collection, override=None)`**: Clones a collection with optional field renaming.
- **`get_field(collection, field)`**: Gets a specific field from a collection.
- **`create_field_dropdown(collection, field_name, dropdown_options, type="string")`**: Creates a dropdown field.
- **`create_field(collection, field_data)`**: Creates a new field in a collection.
- **`update_field(collection, field, field_data)`**: Updates an existing field.
- **`delete_field(collection, field)`**: Deletes a field from a collection.

## Contributing
Contributions to DirectusDK are welcome! Here's how you can contribute:
Fork the repository and clone it locally.
Make your changes, add tests if applicable.
Ensure the code passes all tests (we use pytest).
Submit a pull request with a clear description of what you've done.

License
This project is licensed under the MIT License - see the LICENSE file for details