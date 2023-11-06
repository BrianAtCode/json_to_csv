import csv
class csv_file_manager():
    def __init__(self,file_name,mode):
        self.__file_name = file_name
        self.__mode = mode
        self.__editor = None

    def __enter__(self):
        self.__file = open(self.__file_name,self.__mode)
        if self.__mode in ['w', 'w+', 'a', 'a+']:
            self.__editor = csv.writer(self.__file)
        return self.__editor
    
    def __exit__(self,type,value,traceback):
        self.__file.close()