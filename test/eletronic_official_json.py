import requests
from ..lib.writer import table_writer, flat_writer

response = requests.post('https://www.clp.com.hk/bin/calculator/tariff/residential', json={
  "StartDate": "20231001000000",
  "TariffType": "DT",
  "OnPeakPeriod": "0000000100",
  "NoOfDays": "32"
})

with open('./test/src/source.json', 'w') as f:
    f.write(response.text)

output_path = './test/result'
with open('./test/src/source.json') as f:
    writer = flat_writer(f, output_path, file_name='bill_data')
    writer.transform()
    writer.write_to_file()
