from abc import ABC, abstractmethod
import json

class csv_transformer(ABC):

    def __init__(self,source_data):
        self.__source_data = json.load(source_data)

    @property
    def source_data(self):
        return self.__source_data
    
    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def write_to_file(self):
        pass