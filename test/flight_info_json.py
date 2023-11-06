from ..lib import json_formatter, csv_file_manager, csv_transformer,json_to_single_csv_writer

with open('./src/data.json') as source_file:
    writer = json_to_single_csv_writer.json_to_single_csv_writer(source_file, file_name='./result/flight_data')
    writer.transform()
    writer.write_to_file()