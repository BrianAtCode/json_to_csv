class json_deconstructor:
    def __init__(self, nested_json):
        # Initializes a json_deconstructor instance with the provided nested JSON data.
        # Stores the nested JSON, initializes empty dicts for tables and fields, 
        # and calls pre_load() on the nested JSON to extract table and field info.
        self.nested_json = nested_json
        self.__tables = {}
        self.__fields = {}
        self.pre_load(nested_json)

    def pre_load(self, nested_json):

        def load_table(nested_json, name='root'):
            #extract tables names
            self.tables[name] = []
            for key, value in nested_json.items():
                if isinstance(value, dict):
                    load_table(value, key)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            load_table(item, key)

        def load_fields(nested_json, name='root'):
            self.fields[name] = []
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
                        index+=1
                    load_fields(value[maxIndex], key)
                elif isinstance(value, dict):
                    load_fields(value, key)
        load_table(nested_json)
        load_fields(nested_json)

    @property
    def tables(self):
        return self.__tables
    @property
    def fields(self):
        return self.__fields