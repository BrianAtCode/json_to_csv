from ..lib.writer import table_writer, flat_writer

output_path = './test/result'
with open('./test/src/data.json') as source_file:
    writer = table_writer(source_file,output_path,has_random_id=False)
    writer.transform()
    writer.write_to_file()