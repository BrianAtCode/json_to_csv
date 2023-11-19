from ..lib.writer import table_writer, flat_writer

example_data = '''
{
    "table":
    {
        "Id":78912,
        "Customer":"Jason Sweet",
        "City":"Rome"
    },
    "table2":
    {
        "Id":78912,
        "Customer":"Jason Sweet",
        "City":"Rome"
    }
}'''

example_data2 = {
                    "table1": 
                    { 
                        "field1": 1, 
                        "field2": 2, 
                        "field3": 3 
                    },
                    "test": [{

                        "table1": 
                        { 
                            "field1": 1, 
                            "field2": 2, 
                            "field3": 3 
                        }
                    }],
                    "table2": 
                    { 
                        "field1": ({

                            "table1":{
                                "field100": 1,
                            }
                        },2,3), 
                        "field2": 3, 
                        "field3": 4 
                    },
                }
example_data3 = (('lion', ['Africa', 'America']), ('lion1',{"asd":(1,2,3)}))

example_data4 = {"lion": [{"years old":12, "name":"leo", "meal":[6,12,19]},{"years old":6,"meal":6, "name":"noah"}] }

# set output csv file path
output_path = './test/result'

# example: table csv file
#writer = table_writer(example_data, output_path, has_random_id=True)
#writer.transform()
#writer.write_to_file()

## example: load from json file
#with open('./test/src/testing_data.json') as f:
#    writer = table_writer(f, output_path)
#    writer.transform()
#    writer.write_to_file()

# example: flatten csv file
writer = flat_writer(example_data4, output_path, file_name='flat_table')
writer.transform()
writer.write_to_file()

# example: manual table 
writer = table_writer(example_data4, output_path, is_manual=True)
writer.transform()
writer.write_to_file()
