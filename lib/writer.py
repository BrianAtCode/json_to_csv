"""
Module: writer
Package Path: json_to_csv\lib\writer.py

This module provides classes for writing transformed data to CSV files.

Classes
------------------
    1. `table_writer`: This class writes transformed data to separate CSV files.
    2. `flat_writer`: This class writes transformed data to a single CSV file.

"""
from . import json_formatter, csv_file_manager, csv_transformer

class table_writer(csv_transformer.csv_transformer):
    """
    A class for writing transformed data to separate CSV files.

    This class extends the functionality of csv_transformer to transform JSON data and write it to
    separate CSV files, one for each table in the transformed data.

    Attributes
    ------------------
        - __has_random_id (bool): Flag to indicate whether to use random IDs for records.
        - __formatted_data (dict): A dictionary to store the formatted data.

    Methods
    ------------------
    1. `transform(self)`: 
    - Method to transform JSON data into a structured format and prepare it for writing to CSV files.
    - Returns: None

    2. `write_to_file(self)`: 
    - Method to write the transformed data to separate CSV files for each table.
    - Returns: None

    Typical Usage
    ------------------
    1. Create an instance of `table_writer` with source JSON data and csv data path.
    2. Call the `transform` method to transform and format the data.
    3. Call the `write_to_file` method to write the data to separate CSV files.

    Example:
    >>> source_data = {
    ...     "table1": {
    ...         "field1": [1, 2, 3],
    ...         "field2": [4, 5, 6]
    ...     },
    ...     "table2": {
    ...         "field3": [7, 8, 9],
    ...         "field4": [10, 11, 12]
    ...     }
    ... }
    >>> output_path = './test/result/table_data'
    >>> writer = table_writer(source_data, output_path, has_random_id=True)
    >>> writer.transform()
    >>> writer.write_to_file()
    """
    def __init__(self, source_data: dict, output_path:str, is_manual: bool = False, has_random_id: bool = False):
        """
        Initializes a table_writer instance with source JSON data and configuration options.

        Args:
            source_data (dict): The source JSON data to transform and write.
            output_path (str): The output path for the CSV files.
            has_random_id (bool): Flag to indicate whether to use random IDs for records.

        Returns: None

        Example: None
        """
        self.__is_manual = is_manual
        if self.__is_manual:
            super().__init__(None, output_path)
            self.manual_data = source_data
        else:
            super().__init__(source_data, output_path)
            self.__formatted_data = {}
        self.__has_random_id = has_random_id

    def transform(self):
        """
        Method to transform JSON data into a structured format for writing.

        Args: None

        Returns: None

        Example:
        >>> source_data = {
        ...     "table1": {
        ...         "field1": [1, 2, 3],
        ...         "field2": [4, 5, 6]
        ...     },
        ...     "table2": {
        ...         "field3": [7, 8, 9],
        ...         "field4": [10, 11, 12]
        ...     }
        ... }
        >>> output_path = './test/result/table_data'
        >>> writer = table_writer(source_data, output_path, has_random_id=True)
        >>> writer.transform()
        >>> # The data is transformed and prepared for writing.
        >>> writer.write_to_file()
        >>> # The data is written to separate CSV files for each table.
        """
        if self.__is_manual == True:
            return

        formatter = json_formatter.json_formatter(self.source_data,self.__has_random_id)
        formatter.json_to_object_list(self.source_data)
        self.__formatted_data = formatter.store

    def write_to_file(self):
        """
        Method to write the transformed data to separate CSV files for each table.

        Args: None

        Returns: None

        Example: 
        >>> source_data = {
        ...     "field1": [1, 2, 3],
        ...     "field2": [4, 5, 6]
        ... }
        >>> output_path = './test/result/table_data'
        >>> writer = table_writer(source_data, output_path, has_random_id=True)
        >>> writer.transform()
        >>> # The data is transformed and prepared for writing.
        >>> writer.write_to_file()
        >>> # The data is written to a single CSV file.
        """
        for key,value in self.__formatted_data.items():
            with csv_file_manager.csv_file_manager(self.output_path + "/" +key + '.csv', 'w') as csv_editor:
                if len(value)>0:
                    keys = value[0].keys()
                    csv_editor.writerow(keys)
                    for item in value:
                        reproduce_obj = {}
                        if item is not None and type(item) is dict:
                            for key_item in keys:
                                for record_key,record_value in item.items():
                                    if record_key == key_item:
                                        reproduce_obj[record_key] = record_value
                                        break
                            csv_editor.writerow(reproduce_obj.values())
        
    @property
    def manual_data(self):
        if self.__is_manual == True:
            return self.source_data
    
    @manual_data.setter
    def manual_data(self, value):

        if self.__is_manual == True:
            self.source_data = value
            self.__formatted_data = self.__check_formatted_data(self.source_data)

    @property
    def is_manual(self):
        return self.__is_manual

    @is_manual.setter
    def is_manual(self, value:bool):
        self.__is_manual = value

    def __check_formatted_data(self, formatted_data:dict):
        if type(formatted_data) is not dict:
            raise TypeError("The formatted data must be a dictionary.")
        
        for key,value in formatted_data.items():
            if type(value) is not list:
                raise TypeError("The value of the formatted data must be a list.")
            
            key_list = []
            for item in value:
                if type(item) is not dict:
                    raise TypeError("The item of the formatted data must be a dictionary.")

                key_list.append(list(item.keys()))

                for key_item,value_item in item.items():
                    if type(value_item) is dict:
                        raise TypeError("The value of the formatted data must be the specified primitive type.")
                    elif type(value_item) is list:
                        if self.__check_formatted_value_list(value_item) == False:
                            raise TypeError("The value of the formatted data must be the specified primitive type.")
            for item in key_list:
                for second_item in key_list:
                    item.sort()
                    second_item.sort()
                    if item != second_item:
                        raise TypeError("The key of the formatted data must be the same.")
        return formatted_data

    def __check_formatted_value_list(self, formatted_value_list:list):
        primitive_type_judger = True
        for item in formatted_value_list:
            if type(item) is dict:
                return False
            elif type(item) is list:
                primitive_type_judger = self.__check_formatted_value_list(item)

        return primitive_type_judger
    
class flat_writer(csv_transformer.csv_transformer):
    """
    A class for writing transformed data to a single CSV file.

    This class extends the functionality of csv_transformer to transform JSON data and write it to
    a single CSV file.

    Attributes
    ------------------
        - __formatted_data (dict): A dictionary to store the formatted data.
        - __file_name (str): The name of the CSV file to write the data to.

    Methods
    ------------------
    1. `transform(self)`: 
    - Method to transform JSON data into a structured format and prepare it for writing to a single CSV file.
    - Returns: None

    2. `write_to_file(self)`: 
    - Method to write the transformed data to a single CSV file.
    - Returns: None

    Typical Usage
    ------------------
    1. Create an instance of `flat_writer` with source JSON data, csv data path and an optional file name.
    2. Call the `transform` method to transform and format the data.
    3. Call the `write_to_file` method to write the data to a single CSV file.

    Example:
    >>> source_data = {
    ...     "field1": [1, 2, 3],
    ...     "field2": [4, 5, 6]
    ... }
    >>> output_path = 'output_data/data'
    >>> writer = flat_writer(source_data, output_path, file_name='output_data')
    >>> writer.transform()
    >>> writer.write_to_file()
    """
    def __init__(self, source_data, output_path, file_name = 'default'):
        """
        Initializes a flat_writer instance with source JSON data and an optional file name.

        Args:
            source_data: The source JSON data to transform and write.
            output_path (str): The path to the output directory.
            file_name (str): The name of the CSV file for writing the data (default is 'default').

        Returns: None

        Example: None
        """
        super().__init__(source_data, output_path)
        self.__formatted_data = {}
        self.__file_name = file_name
    
    def transform(self):
        """
        Method to transform JSON data into a structured format for writing.

        Args: None

        Returns: None

        Example: 
        >>> source_data = {
        ...     "table1": {
        ...         "field1": [1, 2, 3],
        ...         "field2": [4, 5, 6]
        ...     },
        ...     "table2": {
        ...         "field3": [7, 8, 9],
        ...         "field4": [10, 11, 12]
        ...     }
        ... }
        >>> output_path = 'output_data/data'
        >>> writer = flat_writer(source_data, output_path, file_name='output_data')
        >>> writer.transform()
        >>> # The data is transformed and prepared for writing.
        >>> writer.write_to_file()
        >>> # The data is written to separate CSV files for each table.
        """
        formatter = json_formatter.json_formatter(self.source_data)
        formatter.flatten_json(self.source_data)
        self.__formatted_data = formatter.store

    def write_to_file(self):
        """
        Method to write the transformed data to a single CSV file.

        Args: None

        Returns: None

        Example:
        >>> source_data = {
        ...     "field1": [1, 2, 3],
        ...     "field2": [4, 5, 6]
        ... }
        ... output_path = 'output_data/data'
        >>> writer = flat_writer(source_data, output_path, file_name='output_data')
        >>> writer.transform()
        >>> # The data is transformed and prepared for writing.
        >>> writer.write_to_file()
        >>> # The data is written to a single CSV file.
        """
        with csv_file_manager.csv_file_manager(self.output_path + "/" + self.__file_name+'.csv', 'w') as csv_editor:
            csv_editor.writerow(self.__formatted_data.keys())
            csv_editor.writerow(self.__formatted_data.values())
