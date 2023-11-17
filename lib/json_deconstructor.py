"""
Module: json_deconstructor
Package Path: json_to_csv\lib\json_deconstructor.py

This module provides a class for deconstructing nested JSON data into tables and fields.

Class
------------------
    1. `json_deconstructor`: This class deconstructs nested JSON data into tables and fields.

"""
class json_deconstructor:
    """
    A class for deconstructing nested JSON data into tables and fields.

    This class is designed to process nested JSON data and extract relevant tables and fields
    to facilitate data processing and transformation.

    Attributes
    ------------------
        - nested_json (dict): The nested JSON data to be deconstructed.
        - __tables (dict): A dictionary to store tables extracted from the JSON data.
        - __fields (dict): A dictionary to store fields extracted from the JSON data.

    Methods
    ------------------
    1. `pre_load(self, nested_json: dict)`: 
    - Method to preprocess and load tables and fields from the nested JSON data.
    - Arguments:
        - `nested_json` (dict): The nested JSON data to be processed.
    - Returns: None

    Properties
    ------------------
        - tables (dict): Property to access the extracted tables.
        - fields (dict): Property to access the extracted fields.

    Typical Usage
    ------------------
    1. Create an instance of `json_deconstructor` with nested JSON data.
    2. Call the `pre_load` method to preprocess and load tables and fields.
    3. Access the extracted tables and fields using the `tables` and `fields` properties.

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
    >>> deconstructor = json_deconstructor(nested_data)
    >>> deconstructor.pre_load(nested_data)
    >>> tables = deconstructor.tables
    >>> fields = deconstructor.fields
    """
    def __init__(self, nested_json: dict):
        """
        Initializes a json_deconstructor instance with the nested JSON data.

        Args:
            nested_json (dict): The nested JSON data to be deconstructed.

        Returns: None

        Example: None
        """
        self.nested_json = nested_json
        self.__tables = {}
        self.__fields = {}
        
        #self.check_pattern(self.nested_json)
        self.pre_load(nested_json)

    def pre_load(self, nested_json: dict):
        """
        Method to preprocess and load tables and fields from the nested JSON data.

        Args:
            nested_json (dict): The nested JSON data to be processed.

        Returns: None

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
        >>> deconstructor = json_deconstructor(nested_data)
        >>> # Call the pre_load method to extract tables and fields.
        >>> deconstructor.pre_load(nested_data)
        >>> # Access the extracted tables and fields.
        >>> extracted_tables = deconstructor.tables
        >>> extracted_fields = deconstructor.fields
        >>> # Verify the extracted tables and fields.
        >>> print(extracted_tables)
        {'table1': [], 'table2': []}
        >>> print(extracted_fields)
        {'table1': ['field1', 'field2'], 'table2': ['field3', 'field4']}
        """
        def load_table(nested_json, name='root', is_nested_list = False):
            if type(nested_json) is dict:
                self.__tables[name] = []

                for key, value in nested_json.items():
                    if isinstance(value, dict):
                        load_table(value, key)
                    elif isinstance(value, list):
                        list_count = 0
                        for item in value:
                            if isinstance(item, dict):
                                load_table(item, key)
                            elif isinstance(item, list):
                                load_table(item, key+"_"+str(list_count))
                            list_count += 1
            elif type(nested_json) is list:
                list_count = 0
                if is_nested_list == False:
                    for item in nested_json:
                        if isinstance(item, dict):
                            load_table(item, name)
                        elif isinstance(item, list):
                            load_table(item, name+"_"+str(list_count))
                        list_count += 1
                else:
                    self.__tables[name] = []
                    for item in nested_json:
                        if isinstance(item, dict):
                            load_table(item, name)
                        elif isinstance(item, list):
                            load_table(item, name+"_"+str(list_count))
                        list_count += 1

        def load_fields(nested_json, name='root'):
            print('load field', self.__tables, name)
            #if name not in self.__tables.keys():
            #    return
            if type(nested_json) is dict:
                if name not in self.__tables:
                    find_next_fields_from_object(nested_json,name)
                    return
                
                if name not in self.__fields:
                    self.__fields[name] = []
                    self.__fields[name].append("parent_id")
                    self.__fields[name].append(name+"_id")

                
                for key, value in nested_json.items():
                    if key not in self.__fields[name]:
                        self.fields[name].append(key)
                
                find_next_fields_from_object(nested_json,name)
            elif type(nested_json) is list:
                if is_pure_data_type(nested_json):
                    return
                
                if name not in self.__tables:
                    find_next_fields_from_list(nested_json,name)
                    return
                
                if name not in self.__fields.keys():
                    self.__fields[name] = []
                    self.__fields[name].append("parent_id")
                    self.__fields[name].append(name+"_id")

                for item in extract_keys(nested_json):
                    if item not in self.__fields[name]:
                        self.__fields[name].append(item)   

                find_next_fields_from_list(nested_json,name)

        def find_next_fields(nested_json, name):
            if isinstance(nested_json, list) or isinstance(nested_json, dict):
                load_fields(nested_json,  name)

        def find_next_fields_from_object(nested_json,name):
            for key, value in nested_json.items():
                load_fields(value, key)

        def find_next_fields_from_list(nested_json,name):
            list_count = 0
            for item in nested_json:
                find_next_fields(item,  name+"_"+str(list_count))
                list_count += 1

        def is_pure_data_type(json_list):
            list_and_dict_count = [type(next_value) for next_value in json_list].count(list) + [type(next_value) for next_value in json_list].count(dict)
            return list_and_dict_count == 0
        
        def extract_keys(json_list):
            keys = set()

            for item in json_list:
                if isinstance(item, dict):
                    keys.update(item.keys())

            return list(keys)
        load_table(nested_json)
        print('tables', self.__tables)
        load_fields(nested_json)
        print('fields', self.__fields)
    
    def check_pattern(self, nested_json):
        if type(nested_json) is dict:
            for key, value in nested_json.items():
                if isinstance(value, list):
                    print (value)
                    if self.is_same_pattern(value) == False:
                        raise Exception("The nested JSON data is not in the same pattern.")
                    else:
                        self.check_pattern(value)
                elif isinstance(value, dict):
                    self.check_pattern(value)
        elif type(nested_json) is list:
            for item in nested_json:
                if isinstance(item, dict):
                    self.check_pattern(item)
                elif isinstance(item, list):
                    print ("list in",item)
                    if self.is_same_pattern(item) == False:
                        raise Exception("The nested JSON data is not in the same pattern.")
                    else:
                        self.check_pattern(item)
        

    def is_same_pattern(self, json_list):
        print("is_same", isinstance(json_list, list), not json_list, type(json_list),isinstance(json_list, list))
        if not isinstance(json_list, list):
            print("eeeee", not json_list, not isinstance(json_list, list))
            return False

        pattern = None

        for item in json_list:
            if isinstance(item, dict):
                current_pattern = tuple(sorted(item.keys()))
            elif isinstance(item, list):
                current_pattern = "list"
            else:
                current_pattern = "other"

            if pattern is None:
                pattern = current_pattern
            elif pattern != current_pattern:
                return False

        return True

    @property
    def tables(self) -> dict:
        """
        Property to access the extracted tables.

        Returns:
            dict: A dictionary of extracted tables.

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
        >>> deconstructor = json_deconstructor(nested_data)
        >>> extracted_tables = deconstructor.tables
        >>> # Access the extracted tables as a dictionary.
        >>> print(extracted_tables)
        {'table1': [], 'table2': []}
        ```
        """
        return self.__tables

    @property
    def fields(self) -> dict:
        """
        Property to access the extracted fields.

        Returns:
            dict: A dictionary of extracted fields.

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
            >>> deconstructor = json_deconstructor(nested_data)
            >>> extracted_fields = deconstructor.fields
            >>> # Access the extracted fields as a dictionary.
            >>> print(extracted_fields)
            {'table1': ['field1', 'field2'], 'table2': ['field3', 'field4']}
        """
        return self.__fields
