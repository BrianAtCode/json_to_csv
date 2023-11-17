# A Specific Pattern Of Json Converting To CSV File

## Table of Contents

- [About](#about)
- [Explanation of the Transformation Process](#explanation)
- [Available Json Pattern](#Available_Json_Pattern)
- [Not Available Json Pattern](#Not_Available_Json_Pattern)
- [Getting Started](#getting_started)
- [Usage](#usage)

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

Add notes about how to use the system.
