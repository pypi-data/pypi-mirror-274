def create_table_column_details(path_to_local_parquet_file_with_name):
     import pandas as pd
     import pyarrow as pa
     import pyarrow.parquet as pq
     
     def get_dypes(dtype):
          if dtype == 'O':
               return 'varchar(80)'
          elif dtype == 'int64':
               return 'integer'
          elif dtype == 'int':
               return 'integer'
          elif dtype == 'float64':
               return 'double'
          else:
               return dtype

     parquet_data = pq.ParquetFile(path_to_local_parquet_file_with_name)
     parquet_schema = pa.schema([f.remove_metadata() for f in parquet_data.schema_arrow])
     
     parquet_columns = list()
     parquet_data_types = list()
     for i in parquet_schema:
          parquet_columns.append(i.name)
          parquet_data_types.append(get_dypes(str(i.type)))
     
     column_details_list =list(map(lambda a,b: a + ' ' + str(b), parquet_columns, parquet_data_types)) 
     column_details_string = ", ".join(column_details_list)

     return column_details_string
