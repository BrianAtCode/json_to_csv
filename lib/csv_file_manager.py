import csv

"""csv_file_manager is a context manager to open a CSV file for reading/writing.

Typical usage:

with csv_file_manager(filename, mode) as csv_editor:
    csv_editor.writerow(...)

On entering, it opens the file and returns a csv.writer instance. 
On exiting, it closes the file automatically.
"""
class csv_file_manager():
    def __init__(self,file_name,mode):
        self.__file_name = file_name
        self.__mode = mode
        self.__editor = None

    def __enter__(self):
        self.__file = open(self.__file_name,self.__mode)
        if self.__mode == 'w' or self.__mode == 'w+' or self.__mode == 'a' or self.__mode == 'a+':
            self.__editor = csv.writer(self.__file)
        return self.__editor
    
    def __exit__(self,type,value,traceback):
        self.__file.close()