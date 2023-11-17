"""
Module: json_formatter
Package Path: json_to_csv\lib\json_formatter.py

This module provides a class for formatting and transforming nested JSON data into a structured format.

Class
------------------
    1. `json_formatter`: This class handles the transformation and formatting of nested JSON data.

"""
from . import json_deconstructor
import uuid

class json_formatter:
    """
    A class for formatting and transforming nested JSON data into a structured format.

    This class processes nested JSON data, extracts tables and fields, and formats the data into
    a structured format for further use.

    Attributes
    ------------------
        - json_handler (json_deconstructor.json_deconstructor): An instance of the json_deconstructor class.
        - __store (dict): A dictionary to store the formatted data.
        - random_id (bool): Flag to indicate whether to use random IDs for records.

    Methods
    ------------------
    1. `json_to_object_list(self, x, table_name: str = 'root', parent_id: str = '', id: str = None)`: 
    - Method to transform nested JSON data into a structured format.
    - Arguments:
        - `x`: The JSON data to transform.
        - `table_name` (str): The name of the table being processed.
        - `parent_id` (str): The parent ID of the current record.
        - `id` (str): The record ID.
    - Returns: None

    2. `json_list_standardize(self)`: 
    - Method to standardize the formatted data to ensure consistent fields across records.
    - Returns: None

    3. `flatten_json(self, nested_json, name: str = '')`: 
    - Method to flatten nested JSON data into a structured format.
    - Arguments:
        - `nested_json`: The nested JSON data to flatten.
        - `name` (str): The name of the current field or table.
    - Returns: None

    Properties
    ------------------
        - store (dict): Property to access the formatted data.

    Typical Usage
    ------------------
    1. Create an instance of `json_formatter` with nested JSON data.
    2. Use the `json_to_object_list` method to transform the data into a structured format.
    3. Use the `json_list_standardize` method to standardize the data.
    4. Access the formatted data using the `store` property.

    Example:
    >>> nested_data = {
    ...     "table1": {
    ...         "field1": [1, 2, 3],
    ...         "field2": [4, 5, 6]
    ...     },
    ...     "table2": {
    ...         "field3": [7, 8, 9],
    ...         "field4": [10, 11, 12]
    ...     }
    ... }
    >>> formatter = json_formatter(nested_data, random_id=True)
    >>> formatter.json_to_object_list(nested_data)
    >>> formatter.json_list_standardize()
    >>> formatted_data = formatter.store
    """
    def __init__(self, nested_json: dict, random_id: bool = False):
        """
        Initializes a json_formatter instance with nested JSON data.

        Args:
            nested_json (dict): The nested JSON data to be formatted.
            random_id (bool): Flag to indicate whether to use random IDs for records.

        Returns: None

        Example: None
        """
        self.json_handler = json_deconstructor.json_deconstructor(nested_json)
        self.__store = self.json_handler.tables
        self.random_id = random_id

    def json_to_object_list(self, x, table_name: str = 'root', parent_id: str = '', id: str = None):

        key_count = 0
        new_parent_id = parent_id if table_name != 'root' else ''
        if type(x) is dict:
            json_object = {"parent_id":new_parent_id}
            json_object[table_name+'_id'] = table_name +"_"+str(len(self.__store[table_name])) if self.random_id == False else str(uuid.uuid4()) if id == None else id

            for key,value in x.items():
                if key == json_object[table_name+'_id']:
                    continue
                
                if type(value) is dict:
                    json_object[key] =  key+"_"+str(len(self.__store[key]))  if self.random_id == False else str(uuid.uuid4())
                    self.json_to_object_list(value, key, json_object[table_name+'_id'], json_object[key])

                elif type(value) is list:
                    pure_value = self.get_pure_value_from_object(key, value, table_name)
                    if pure_value:
                        json_object[key] = pure_value
                    else:
                        json_object[key] = key+"_"+str(len(self.__store[key]))   if self.random_id == False else str(uuid.uuid4())

                    self.json_to_object_list(value, key, json_object[key], None)
                else:
                    json_object[key] = value
            print('122', json_object)
            for key in self.json_handler.fields[table_name]:
                if key not in json_object.keys():
                    json_object[key] = ''

            self.__store[table_name].append(json_object)
        elif type(x) is list:
            list_and_dict_count = [type(next_value) for next_value in x].count(list) + [type(next_value) for next_value in x].count(dict)
            if list_and_dict_count == 0:
                return
            
            for a in x:
                if type(a) is dict:
                    self.json_to_object_list(a, table_name, parent_id, None)
                elif type(a) is list:
                    next_key = table_name+"_"+str(key_count)+"_"+str(len(self.__store[table_name]))  if self.random_id == False else str(uuid.uuid4())
                    self.json_to_object_list(a, table_name+"_"+str(key_count), next_key, None)
                key_count += 1
    def get_pure_value(self, value):
        return [type(next_value) for next_value in value].count(list) + [type(next_value) for next_value in value].count(dict)
   
    def get_pure_value_from_object(self,key, value, table_name ):
        list_and_dict_count = self.get_pure_value(value)
        if key not in self.__store[table_name] and list_and_dict_count == 0:
            return ", ".join([str(new_val) for new_val in value]) 

        return None
    
    def json_list_standardize(self):
        """
        Method to standardize the formatted data to ensure consistent fields across records.

        Returns: None

        Example: 
        >>> source_data = {
        ...     "table1": {
        ...         "field1": [1, 2, 3],
        ...         "field2": [4, 5, 6]
        ...     }
        ... }
        >>> formatter = json_formatter(source_data)
        >>> # Call the json_to_object_list method to transform the data.
        >>> formatter.json_to_object_list(source_data, table_name='table1')
        >>> # Call the json_list_standardize method to standardize the fields.
        >>> formatter.json_list_standardize()
        >>> # Access the standardized data using the store property.
        >>> standardized_data = formatter.store
        >>> # Verify the standardized data.
        >>> print(standardized_data)
        {'table1': [{'table1_id': 'table1_0', 'field1': 1, 'field2': 4}, {'table1_id': 'table1_1', 'field1': 2, 'field2': 5}, {'table1_id': 'table1_2', 'field1': 3, 'field2': 6}]}
        """
        print('standard item',self.__store)
        for key, value in self.json_handler.fields.items():
            print('key', key, 'value', value)
            count = 0
            for item in self.__store[key]:
                for field in value:
                    if type(field) is not dict or type(field) is not list:
                        if field not in item:
                            self.__store[key][count][field] = ''
                count+=1

    def flatten_json(self, nested_json, name: str = ''):
        """
        Method to flatten nested JSON data into a structured format.

        Args:
            nested_json: The nested JSON data to flatten.
            name (str): The name of the current field or table.

        Returns: None

        Example: 
        >>> source_data = {
        ...     "table1": {
        ...         "field1": [1, 2, 3],
        ...         "field2": [4, 5, 6]
        ...     }
        ... }
        >>> formatter = json_formatter(source_data)
        >>> # Call the flatten_json method to flatten the data.
        >>> formatter.flatten_json(source_data)
        >>> # Access the flattened data using the store property.
        >>> flattened_data = formatter.store
        >>> # Verify the flattened data.
        >>> print(flattened_data)
        {'table1_field1_0': 1, 'table1_field1_1': 2, 'table1_field1_2': 3, 'table1_field2_0': 4, 'table1_field2_1': 5, 'table1_field2_2': 6}
        """
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
    def store(self) -> dict:
        """
        Property to access the formatted data.

        Returns:
            dict: The formatted data.

        Example: None
        """
        return self.__store
