## Example Usage

If you want to run the file from the test folder, you should create the empty python file outside the json_to_csv folder, then write the below code in the file and run it.

```
import json_to_csv.test.json2csv
```

If you are try to create a test file inside the test folder, you should import the test file like below.

```
from ..lib.writer import table_writer, flat_writer
```