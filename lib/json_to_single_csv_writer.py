

from . import json_formatter, csv_file_manager, csv_transformer

class json_to_single_csv_writer(csv_transformer.csv_transformer):
    def __init__(self, source_data, file_name = 'default'):
        super().__init__(source_data)
        self.__formatted_data = {}
        self.__file_name = file_name
    
    def transform(self):
        formatter = json_formatter.json_formatter(self.source_data)
        formatter.flatten_json(self.source_data)
        self.__formatted_data = formatter.store
    
    def write_to_file(self):
        with csv_file_manager.csv_file_manager(self.__file_name+'.csv', 'w') as csv_editor:
            csv_editor.writerow(self.__formatted_data.keys())
            csv_editor.writerow(self.__formatted_data.values())

    