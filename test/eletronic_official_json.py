import requests
from ..lib import json_formatter, csv_file_manager, csv_transformer,json_to_single_csv_writer

response = requests.post('https://www.clp.com.hk/bin/calculator/tariff/residential', json={
  "StartDate": "20231001000000",
  "TariffType": "DT",
  "OnPeakPeriod": "0000000100",
  "NoOfDays": "32"
})

with open('./src/source.json', 'w') as f:
    f.write(response.text)

with open('./src/source.json') as f:
    writer = json_to_single_csv_writer.json_to_single_csv_writer(f, file_name='./result/bill_data')
    writer.transform()
    writer.write_to_file()
