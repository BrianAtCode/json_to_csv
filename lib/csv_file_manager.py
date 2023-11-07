"""
Module: csv_file_manager
package path: lib\csv_file_manager.py

This module provides a CSV file management class for reading and writing CSV files.

Class
------------------
    1. `csv_file_manager`: This class provides methods for creating and managing CSV files.

"""
import csv
class csv_file_manager:
    """
    A utility class for managing CSV files using the CSV module.

    This class allows you to create, open, and interact with CSV files in various modes,
    such as read, write, append, and more.
    
    Attributes
    ------------------
        - __file_name (str): The name of the CSV file to be managed.
        - __mode (str): The file access mode, which can be 'w', 'w+', 'a', or 'a+'.
        - __editor: A CSV writer instance used to write data to the CSV file.
        
    Methods
    ------------------
    1. `__init__(self, file_name: str, mode: str)`: 
    - Constructor to initialize the CSV file manager.
    - Arguments:
        - `file_name` (str): The name of the CSV file.
        - `mode` (str): The mode for opening the file ('w', 'w+', 'a', 'a+').
    - Returns: None

    2. `__enter__(self) -> csv.writer or None`:
    - Context manager method to open the CSV file.
    - Returns:
        - `csv.writer` or None: Returns the CSV writer if the file is opened successfully; otherwise, None.

    3. `__exit__(self, type, value, traceback) -> None`:
    - Context manager method to close the CSV file.
    - Arguments:
        - `type`: The type of exception, if any.
        - `value`: The exception object, if any.
        - `traceback`: The traceback object.
    - Returns: None

    Typical Usage
    ------------------
    1. Create an instance of csv_file_manager with the desired file name and mode.
    2. Use the instance as a context manager to open the CSV file and get a writer instance.
    3. Perform write operations on the CSV file within the context block.
    4. The file is automatically closed upon exiting the context block.

    Example:
    >>> # Creating a CSV file manager instance
    ... with csv_file_manager('example.csv', 'w') as writer:
    ...     writer.writerow(['Name', 'Age'])
    ...     writer.writerow(['Alice', 25])
    ...     writer.writerow(['Bob', 30])
    >>> # 'example.csv' is closed after the context block.
    """
    def __init__(self, file_name, mode):
        """
        Initializes a csv_file_manager instance with the specified file name and mode.

        Args:
            file_name (str): The name of the CSV file to work with.
            mode (str): The file access mode ('r' for read, 'w' for write, 'a' for append, etc.).
        
        Returns: None

        Example: None
        """
        self.__file_name = file_name
        self.__mode = mode
        self.__editor = None

    def __enter__(self):
        """
        Enters the context manager, opening the CSV file in the specified mode.

        Args: None

        Returns:
            csv.writer: A CSV writer instance if the mode is for writing, None for reading.

        Example:
        >>> with csv_file_manager('example.csv', 'w') as writer:
        ...     # Perform write operations using 'writer' within this block.
        """
        self.__file = open(self.__file_name, self.__mode)
        if self.__mode in ['w', 'w+', 'a', 'a+']:
            self.__editor = csv.writer(self.__file)
        return self.__editor

    def __exit__(self, type, value, traceback):
        """
        Exits the context manager and closes the CSV file.

        Args:
            type: The type of exception raised (if any).
            value: The exception object (if any).
            traceback: The traceback information (if any).
        
        Returns: None

        Example:
        >>> # The CSV file is automatically closed upon exiting the context block.
        >>> with csv_file_manager('example.csv', 'w') as writer:
        ...     writer.writerow(['Name', 'Age'])
        ...     writer.writerow(['Alice', 25])
        >>> # 'example.csv' is closed after the context block.
        """
        self.__file.close()
