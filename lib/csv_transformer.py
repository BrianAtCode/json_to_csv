"""
Module: csv_transformer
Package Path: json_to_csv\lib\csv_transformer.py

This module provides an abstract base class for transforming JSON data into CSV format.

Class
------------------
    1. `csv_transformer`: This abstract base class defines methods for transforming JSON data to CSV.

"""
from abc import ABC, abstractmethod
import json

class csv_transformer(ABC):
    """
    An abstract base class for transforming JSON data into CSV format.

    This class defines methods for loading source JSON data, transforming it into a suitable format
    for CSV, and writing the transformed data to a CSV file.

    Attributes
    ------------------
        - __source_data (dict): The source JSON data to be transformed into CSV format.
        - __output_path (str): The output path for the CSV file.

    Properties
    ------------------
        - source_data (dict): Property to access the source JSON data.
        - output_path (str): Property to access the output path for the CSV file.

    Abstract Methods
    ------------------
    1. `transform(self) -> None`: 
    - Abstract method to transform the JSON data into a format suitable for CSV.
    - Returns: None

    2. `write_to_file(self) -> None`:
    - Abstract method to write the transformed data to a CSV file.
    - Returns: None

    Typical Usage
    ------------------
    1. Create a subclass of `csv_transformer` and implement the `transform` and `write_to_file` methods.
    2. Load source JSON data and use the subclass to perform the transformation and write to a CSV file.

    Example:
    >>> class MyCsvTransformer(csv_transformer):
    ...     def transform(self):
    ...         # Implement JSON to CSV transformation logic here
    ...         pass
    ...
    ...     def write_to_file(self):
    ...         # Implement writing the transformed data to a CSV file here
    ...         pass
    ...
    >>> source_data = {
    ...     "data": [
    ...         {"name": "Alice", "age": 30},
    ...         {"name": "Bob", "age": 25}
    ...     ]
    ... }
    ... output_path = 'output_data/data'
    >>> transformer = MyCsvTransformer(source_data, output_path)
    >>> transformer.transform()
    >>> transformer.write_to_file()
    """

    def __init__(self, source_data: dict, output_path: str = ''):
        """
        Initializes a csv_transformer instance with the source JSON data.

        Args:
            source_data (dict): The source JSON data to be transformed into CSV format.
            output_path (str): The output path for the CSV file (default is '').

        Returns: None

        Example: None
        """
        self.__output_path = output_path

        if source_data is None:
            return
        decoder = json.JSONDecoder(object_pairs_hook=self.__checking_duplicate_value)

        if type(source_data).__name__== 'TextIOWrapper':
            self.__source_data = json.load(source_data)
        elif type(source_data).__name__== 'dict' or type(source_data).__name__== 'list':
            self.__source_data = json.loads(json.dumps(source_data))
        elif type(source_data).__name__ == 'tuple':
            to_dict = dict( (key ,value) for key,value in source_data)
            self.__source_data = json.loads(json.dumps(to_dict))
        elif type(source_data).__name__== 'str':
            self.__source_data = decoder.decode(source_data)
        else:
            raise TypeError("The source data must be a dict or a file-like object.")

    def __checking_duplicate_value(self,pairs):
        result = dict()
        for key,val in pairs:
            if key in result:
                raise KeyError("Duplicate key specified: %s" % key)
            result[key] = val
        return result
    @property
    def source_data(self) -> dict:
        """
        Property to access the source JSON data.

        Returns:
            dict: The source JSON data.

        Example: None
        """
        return self.__source_data
    
    @source_data.setter
    def source_data(self, source_data: dict) -> None:
        """
        Property to set the source JSON data.

        Args:
            source_data (dict): The source JSON data to be transformed into CSV format.

        Returns: None

        Example: None
        """
        self.__source_data = source_data

    @property
    def output_path(self) -> str:
        """
        Property to access the output path for the CSV file.

        Returns:
            str: The output path for the CSV file.

        Example: None
        """
        return self.__output_path

    @abstractmethod
    def transform(self) -> None:
        """
        Abstract method to transform the JSON data into a format suitable for CSV.

        Args: None

        Returns: None

        Example: None
        """
        pass

    @abstractmethod
    def write_to_file(self) -> None:
        """
        Abstract method to write the transformed data to a CSV file.

        Args: None

        Returns: None

        Example: None
        """
        pass
