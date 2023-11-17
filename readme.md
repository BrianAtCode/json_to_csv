# Convert Json to Csv 

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

This is a python script that support converting json data to structured csv file, transforming json to different format of csv data, such as table and flatten format. According to the loaded json, the script also support any content of nested json convert to csv file.

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
writer = table_writer(source_data, output_path, has_random_id=True is_standardize=True)
writer.transform()
writer.write_to_file()
```
## Usage <a name = "usage"></a>

Add notes about how to use the system.
