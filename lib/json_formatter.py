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
    1. `json_to_object__list(self, x, table_name: str = 'root', parent_id: str = '', id: str = None)`: 
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
    2. Use the `json_to_object__list` method to transform the data into a structured format.
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
    >>> formatter.json_to_object__list(nested_data)
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
        self.__store = {}
        self.random_id = random_id

    def json_to_object__list(self, x, table_name: str = 'root', parent_id: str = '', id: str = None):
        """
        Method to transform nested JSON data into a structured format.

        Args:
            x: The JSON data to transform.
            table_name (str): The name of the table being processed.
            parent_id (str): The parent ID of the current record.
            id (str): The record ID.

        Returns: None

        Example: 
            >>> source_data = {
            ...     "table1": {
            ...         "field1": [1, 2, 3],
            ...         "field2": [4, 5, 6]
            ...     }
            ... }
            >>> formatter = json_formatter(source_data)
            >>> # Call the json_to_object__list method to transform the data.
            >>> formatter.json_to_object__list(source_data, table_name='table1')
            >>> # Access the transformed data using the store property.
            >>> transformed_data = formatter.store
            >>> # Verify the transformed data.
            >>> print(transformed_data)
            {'table1': [{'table1_id': 'table1_0', 'field1': 1, 'field2': 4}, {'table1_id': 'table1_1', 'field1': 2, 'field2': 5}, {'table1_id': 'table1_2', 'field1': 3, 'field2': 6}]}
        """
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
        >>> # Call the json_to_object__list method to transform the data.
        >>> formatter.json_to_object__list(source_data, table_name='table1')
        >>> # Call the json_list_standardize method to standardize the fields.
        >>> formatter.json_list_standardize()
        >>> # Access the standardized data using the store property.
        >>> standardized_data = formatter.store
        >>> # Verify the standardized data.
        >>> print(standardized_data)
        {'table1': [{'table1_id': 'table1_0', 'field1': 1, 'field2': 4}, {'table1_id': 'table1_1', 'field1': 2, 'field2': 5}, {'table1_id': 'table1_2', 'field1': 3, 'field2': 6}]}
        """
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
