# A Specific Pattern Of Json Converting To CSV File

## Table of Contents

- [About](#about)
- [Explanation of the Transformation Process](#explanation)
- [Available Json Pattern](#Available_Json_Pattern)
- [Not Available Json Pattern](#Not_Available_Json_Pattern)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Do’s and Don’ts](#Dos_and_donts)
- [Reference](#reference)

## About <a name = "about"></a>

This is a python script that support converting some kind of [nested json data](#Available_Json_Pattern) to well-formatted dictionary and CSV file. The format of json is following by **RFC 7159**. The script can search the object inside the nested json data and classify them. As the result, the script output the well-formatted dictionary which is classified by the key and we can choose to export the data to CSV file. Further explanation of the transformation process is provided [below](#explanation).

## Explanation of the Transformation Process <a name = "explanation"></a>
This explanation is about the **json_to_object_list** function of the script mainly.

First of all, the script would treat all the object as a table record and the key of the previous level object would be the table name of this level object. Moreover, the script will assign the id of current level object to the next level object as parent id. The **"parent_id"** and **"table_id"** can be used for portioning the original json data. 

For handling the list, the script will create the table name accord to the level count of the list. Next, it will collect the object and assign those object to the relational table inside the list. 

Then, the script will merge the object key if they have the same table name. After that, the script normalize the record and put it to a proper position. Therefore, some table record will have empty value but the key remain.

After all, the script can be export the data to CSV file.

In additional, the table id or parent id can change to the random id optionally if the table id Collide each other.

## Available Json Pattern <a name = "Available_Json_Pattern"></a>
This part is about the available json pattern that the script can handle.
1. **symmetrical json list**
```
[
    {
        "table1": 
        { 
            "field1": 1, 
            "field2": 2, 
            "field3": 3 
        }
    },
    {
        "table1": 
        {
            "field1": 5,
            "field2": 6,
            "field3": 7,
        }
    }
]
```
2. **non-symmetrical json list**
```
[
    {
        "table1": 
        { 
            "field1": 1, 
            "field2": 2, 
            "field3": 3 
        }
    },
    {
        "table1": 
        {
            "field1": [1,2,3],
            "field2": "abc",
            "field3": [
                {"hello": "world"},
            ],
        }
    }
]
```

## Not Available Json Pattern <a name = "Not_Available_Json_Pattern"></a>

1. **non-symmetrical json list**
```
[
    {
        "table1": 
        { 
            "field1": 1, 
            "field2": 2, 
            "field3": 3 
        }
    },
    5
]
```

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The environment need to install python3.6 or above.

### Installing

A step by step series of examples that tell you how to get a development env running.

1. **Create a library folder inside you project**
```
# go to your project directory
cd {project name}

# create a library folder
mkdir lib

# go to library folder
cd lib
```

2. **download the library to your project folder**
```
git clone https://github.com/BrianAtCode/json_to_csv
```

3. **Import to your codebase**
```
# Import the writer module
from json_to_csv import writer
```

Or 

```
# Import full package
import json_to_csv
```

End with an example of getting some data out of the system or using it for a little demo.
```
# Configure output path
output_path = './test/result'

# Configure output file name
writer = table_writer(source_data, output_path, has_random_id=True)
writer.transform()
writer.write_to_file()
```
## Usage <a name = "usage"></a>
Here are two methods to convert your data to csv file mainly:

1. **``table_writer``** - to convert json data to table format
```
#json string
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

# set output csv file path
output_path = './test/result'

# loading the json file
with open('./test/src/testing_data.json') as f:
    
    # create writer object
    writer = table_writer(f, output_path)
    
    # transform the json data to csv file
    writer.transform()

    # write the csv file
    writer.write_to_file()

### output
#----------------------------------------------
## root table
# parent_id,root_id,table,table2
# ,root_0,table_0,table2_0
#----------------------------------------------
## table table
#parent_id,table_id,Id,Customer,City
#root_0,table_0,78912,Jason Sweet,Rome
#----------------------------------------------
## table2 table
#parent_id,table2_id,Id,Customer,City
#root_0,table2_0,78912,Jason Sweet,Rome
```
2. **``flat_writer``** - to convert json to flatten format
```
# dictionary data
example_data4 = {"lion": [{"years old":12, "name":"leo", "meal":[6,12,19]},{"years old":6,"meal":6, "name":"noah"}] }

# set output csv file path
output_path = './test/result'

# create flat writer object
writer = flat_writer(example_data4, output_path, file_name='flat_table')

# transform the json data to csv file
writer.transform()

# write the csv file
writer.write_to_file()

###output
#----------------------------------------------
## flat_table file
#lion_0_years old,lion_0_name,lion_0_meal_0,lion_0_meal_1,lion_0_meal_2,lion_1_years old,lion_1_meal,lion_1_name
#12,leo,6,12,19,6,6,noah
```

Here are the main options to configure the output csv file.

1. **``has_random_id``** - to assign random id to the table id
```
## this example is base on the example above
...
writer = table_writer(example_data4, output_path, has_random_id=True)
...

### output
## root table
# parent_id,root_id,table,table2
# ,194e47e5-3c2f-4529-a1db-bad11045aaef,eca3c05f-8139-48bc-a790-88ad2b6da453,85134275-1588-4fc0-a59b-b94fbb9885f1
...
```
2. **``is_manual``** - turn on the manual mode to assign the table object manually
```
## this example is base on the example above
example_data4 = {"lion": [{"years old":12, "name":"leo", "meal":[6,12,19]},{"years old":6,"meal":6, "name":"noah"}] }

...
writer = table_writer(example_data4, output_path, is_manual=True)
...

###output
## lion table
#years old,name,meal
#12,leo,"[6, 12, 19]"
#6,noah,6
```

You can get or set some main variables before or after the transformation.

1. **``source_data``** - the original formatted data of json, dictionary, tuple and list
    - **type** : dict (default) 
2. **``output_path``** - the output path of the csv file
    - **type** : str (default: './')
3. **``is_manual``** - turn on the manual mode to assign the table object manually
    - **type** : boolean (default: False)
4. **``manual_data``** - the manual data that you want to replace the source data
    - **type** : dict (default: None)

**More examples can be found in the [test folder](https://github.com/BrianAtCode/json_to_csv/tree/main/test)**

## Do’s and Don’ts <a name = "dos_and_donts"></a>
1. Do not use the same table name in different tables in **``source_data``** or **``manual_data``**
2. Do not use the same field name in different tables in **``manual_data``**
3. Please following the json pattern to avoid the error while the manual mode is on.
4. Do not use the dict type inside the table items of **``manual_data``** 
5. Please use the same key inside the table items of **``manual_data``**

## Reference <a name = "reference"></a>
1. [json string key duplication](https://stackoverflow.com/questions/16172011/json-in-python-receive-check-duplicate-key-error)
2. [code documentary comment](https://chat.openai.com/)