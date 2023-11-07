from ..lib.writer import table_writer, single_csv_writer

with open('./test/src/data.json') as source_file:
    writer = table_writer(source_file)
    writer.transform()
    writer.write_to_file()