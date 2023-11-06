"""
Converts JSON data to CSV format by first normalizing the JSON into a structured list of objects, with unique IDs and parent-child relationships. 

The structured JSON can then be written out to multiple CSV files, one per JSON array/table. Before writing, the structured JSON is standardized by filling any missing fields across rows.

Parameters:

- source_data: The input nested JSON data to convert.

- is_standardize: Whether to standardize the JSON rows before writing CSV.

- has_random_id: Whether to generate random UUIDs for IDs instead of numeric IDs.
"""
from . import json_formatter
from . import csv_file_manager
from . import csv_transformer

class json_to_csv_table_writer(csv_transformer.csv_transformer):
    def __init__(self,source_data,is_standardize=True, has_random_id=False):
        super().__init__(source_data)
        self.__has_random_id=has_random_id 
        self.__is_standardize = is_standardize
        self.__formatted_data = {}
    
    def transform(self):
        formatter = json_formatter.json_formatter(self.source_data,self.__has_random_id)
        formatter.json_to_object__list(self.source_data)
        if self.__is_standardize:
            formatter.json_list_standardize()
        self.__formatted_data = formatter.store

    def write_to_file(self):
        for key,value in self.__formatted_data.items():
            with csv_file_manager.csv_file_manager(key + '.csv', 'w') as csv_editor:
                csv_editor.writerow(value[0].keys())
                for item in value:
                    csv_editor.writerow(item.values())
        print(self.__formatted_data)