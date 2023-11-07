"""
Module: writer
Package Path: json_to_csv\lib\writer.py

This module provides classes for writing transformed data to CSV files.

Classes
------------------
    1. `table_writer`: This class writes transformed data to separate CSV files.
    2. `single_csv_writer`: This class writes transformed data to a single CSV file.

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
        - __is_standardize (bool): Flag to indicate whether to standardize the fields in the data.
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
    >>> writer = table_writer(source_data, output_path, has_random_id=True, is_standardize=True)
    >>> writer.transform()
    >>> writer.write_to_file()
    """
    def __init__(self, source_data: dict, output_path:str, is_standardize: bool = True, has_random_id: bool = False):
        """
        Initializes a table_writer instance with source JSON data and configuration options.

        Args:
            source_data (dict): The source JSON data to transform and write.
            output_path (str): The output path for the CSV files.
            is_standardize (bool): Flag to indicate whether to standardize the fields.
            has_random_id (bool): Flag to indicate whether to use random IDs for records.

        Returns: None

        Example: None
        """
        super().__init__(source_data, output_path)
        self.__has_random_id = has_random_id
        self.__is_standardize = is_standardize
        self.__formatted_data = {}

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
        >>> writer = table_writer(source_data, output_path, has_random_id=True, is_standardize=True)
        >>> writer.transform()
        >>> # The data is transformed and prepared for writing.
        >>> writer.write_to_file()
        >>> # The data is written to separate CSV files for each table.
        """
        formatter = json_formatter.json_formatter(self.source_data,self.__has_random_id)
        formatter.json_to_object__list(self.source_data)
        if self.__is_standardize:
            formatter.json_list_standardize()
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
        >>> writer = table_writer(source_data, output_path, has_random_id=True, is_standardize=True)
        >>> writer.transform()
        >>> # The data is transformed and prepared for writing.
        >>> writer.write_to_file()
        >>> # The data is written to a single CSV file.
        """
        for key,value in self.__formatted_data.items():
            with csv_file_manager.csv_file_manager(self.output_path + "/" +key + '.csv', 'w') as csv_editor:
                csv_editor.writerow(value[0].keys())
                for item in value:
                    csv_editor.writerow(item.values())
        print(self.__formatted_data)

class single_csv_writer(csv_transformer.csv_transformer):
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
    1. Create an instance of `single_csv_writer` with source JSON data, csv data path and an optional file name.
    2. Call the `transform` method to transform and format the data.
    3. Call the `write_to_file` method to write the data to a single CSV file.

    Example:
    >>> source_data = {
    ...     "field1": [1, 2, 3],
    ...     "field2": [4, 5, 6]
    ... }
    >>> output_path = 'output_data/data'
    >>> writer = single_csv_writer(source_data, output_path, file_name='output_data')
    >>> writer.transform()
    >>> writer.write_to_file()
    """
    def __init__(self, source_data, output_path, file_name = 'default'):
        """
        Initializes a single_csv_writer instance with source JSON data and an optional file name.

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
        >>> writer = single_csv_writer(source_data, output_path, file_name='output_data')
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
        >>> writer = single_csv_writer(source_data, output_path, file_name='output_data')
        >>> writer.transform()
        >>> # The data is transformed and prepared for writing.
        >>> writer.write_to_file()
        >>> # The data is written to a single CSV file.
        """
        with csv_file_manager.csv_file_manager(self.output_path + "/" + self.__file_name+'.csv', 'w') as csv_editor:
            csv_editor.writerow(self.__formatted_data.keys())
            csv_editor.writerow(self.__formatted_data.values())
