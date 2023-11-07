import requests
from ..lib.writer import table_writer, single_csv_writer

response = requests.post('https://www.clp.com.hk/bin/calculator/tariff/residential', json={
  "StartDate": "20231001000000",
  "TariffType": "DT",
  "OnPeakPeriod": "0000000100",
  "NoOfDays": "32"
})

with open('./test/src/source.json', 'w') as f:
    f.write(response.text)

with open('./test/src/source.json') as f:
    writer = single_csv_writer(f, file_name='./test/result/bill_data')
    writer.transform()
    writer.write_to_file()
