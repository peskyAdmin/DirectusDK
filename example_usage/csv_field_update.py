import csv

from directusDK.directusDK import DirectusDK
from DIRECTUS_VARIABLES import DIRECTUS_URL, DIRECTUS_KEY

# Create a new instance of the DirectusDK class
directus = DirectusDK(DIRECTUS_URL, DIRECTUS_KEY)
csv_file_path = 'sku_min_quantity.csv'

# CSV to item field
def csv_to_item_field(csv_file_path, directus, collection, field_name):
    problem_items = []

    # build item_id list lookup in this example we are using creating a mapping of sku to id
    # this is a dictionary that will be used to look up the item id based on the sku
    id_sku_lookup = {}
    items = directus.get_all_items(collection)
    for item in items:
        id_sku_lookup[item['sku']] = item['id']

    with open(csv_file_path, newline='') as csvfile:                # open the csv file
        reader = csv.DictReader(csvfile)                            # create a csv reader object
        for row in reader:                                          # iterate over the rows in the csv file
            sku = row['sku']                                        # get the sku from the row
            if sku not in id_sku_lookup:                            # check if the sku is in the id_sku_lookup
                print(f'CSV item with sku {sku} not found in in directus collection {collection}')
                problem_items.append(sku)                           # add the sku to the problem_items list
                continue                                            # skip to the next row      
            else:                                                   # if the sku is in the id_sku_lookup
                item_id = id_sku_lookup[sku]                        # get the item id from the id_sku_lookup
            field_value = row['min_quantity']                       # get the field value from the row labeled 'min_quantity'
            attributes = {field_name: field_value}                  # create a dictionary with the field name and value
            res = directus.update_item(collection=collection,       # update the item in directus
                                       item_id=item_id, 
                                       attributes=attributes)
            print(f'Updated item {item_id} with field {field_name} and value {field_value}')

    with open('problem_items.csv', 'w') as f:                       # write the problem items to a csv file
        for item in problem_items:                                  # iterate over the problem items
            f.write("%s\n" % item)                                  # write the item to the file

# Usage
csv_to_item_field(csv_file_path, directus, collection='collection_name', field_name='min_quantity')



