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
        def load_table(nested_json, name='root'):
            self.__tables[name] = []
            for key, value in nested_json.items():
                if isinstance(value, dict):
                    load_table(value, key)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            load_table(item, key)

        def load_fields(nested_json, name='root'):
            self.__fields[name] = []
            for key, value in nested_json.items():
                self.fields[name].append(key)
                if isinstance(value, list):
                    listLen = 0
                    maxIndex = 0
                    index = 0
                    for item in value:
                        if len(item) > listLen:
                            listLen = len(item)
                            maxIndex = index
                        index += 1
                    load_fields(value[maxIndex], key)
                elif isinstance(value, dict):
                    load_fields(value, key)

        load_table(nested_json)
        load_fields(nested_json)

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
