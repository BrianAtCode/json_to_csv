"""
The json_formatter class provides functionality to flatten nested JSON data into a normalized structure.

The key methods are:

- flatten_json: Flattens the nested JSON into a flat dictionary structure.

- json_to_object_list: Converts the nested JSON into a normalized list of objects structure. This generates a structured format with unique IDs and parent-child relationships.

- json_list_standardize: Standardizes the list of objects by filling in any missing fields. 

The flattened or structured JSON data is stored in the store property.
"""

from . import json_deconstructor
import uuid

class json_formatter:
    def __init__(self, nested_json, random_id=False):
        self.json_handler = json_deconstructor.json_deconstructor(nested_json)
        self.__store = {}
        self.random_id = random_id
    
    def json_to_object__list(self,x,table_name='root', parent_id='',id=None):
        if table_name=='root':
            self.__store = self.json_handler.tables 

        key_count = 0
        rows = [{} if table_name == 'root' else {'parent_id': parent_id} ]
        if type(x) is dict:
            rows[0][table_name+'_id'] = table_name +"_"+str(len(self.__store[table_name])) if self.random_id == False else str(uuid.uuid4()) if id == None else id
            print(27, table_name+'_id', x)
            for key,value in x.items():
                if key == rows[0][table_name+'_id']:
                    continue
                if type(value) is dict:
                    rows[0][key] = key+"_"+str(len(self.__store[key]))   if self.random_id == False else str(uuid.uuid4())
                    self.json_to_object__list(value, key, rows[0][table_name+'_id'], rows[0][key])
                elif type(value) is list:
                    rows[0][key] = key+"_"+str(len(self.__store[key]))   if self.random_id == False else str(uuid.uuid4())
                    self.json_to_object__list(value, key, rows[0][key], None)
                else:
                    rows[0][key] = value
            self.__store[table_name].append(rows[0])
        elif type(x) is list:
            print(31, 'list')
            rows = [{} if table_name == 'root' else {'parent_id': parent_id} for i in range(len(x))]
            for a in x:
                rows[key_count][table_name+'_id'] = table_name +"_"+str(len(self.__store[table_name]))  if self.random_id == False else str(uuid.uuid4()) if id == None else id
                if type(a) is dict:
                    for key,value in a.items():
                        if type(value) is dict:
                            rows[key_count][key] = key+"_"+str(len(self.__store[table_name]))  if self.random_id == False else str(uuid.uuid4())
                            self.json_to_object__list(value, key, rows[key_count][table_name+'_id'], rows[key_count][key])
                        elif type(value) is list:
                            rows[key_count][key] = key+"_"+str(len(self.__store[table_name]))  if self.random_id == False else str(uuid.uuid4())
                            self.json_to_object__list(value, key, rows[key_count][key], None)
                        else:
                            rows[key_count][key] = value
                    self.__store[table_name].append(rows[key_count])
                key_count += 1

    def json_list_standardize(self):
        for key, value in self.json_handler.fields.items():
            print('key', key, 'value', value)
            count = 0
            for item in self.__store[key]:
                print('item',item)
                for field in value:
                    if field not in item:
                        print('not in',field,field,self.__store[key][count])
                        self.__store[key][count][field] = ''
                        print('after append item',self.__store[key])
                count+=1

    def flatten_json(self, nested_json, name=''):
        if type(nested_json) is dict:
            for a in nested_json:
                self.flatten_json(nested_json[a], name + a + '_')
        elif type(nested_json) is list:
            i = 0
            for a in nested_json:
                self.flatten_json(a, name + str(i) + '_')
                i += 1
        else:
            self.__store[name[:-1]] = nested_json

    @property
    def store(self):
        return self.__store