 
def verify_table_fields_with_config(BASE_PATH, table_name, path_to_local_csv_file):
     import pandas as pd
     import json
     
     local_file_df = pd.read_csv(path_to_local_csv_file)
     
     table_schema_path = BASE_PATH +  "/athena_code/" + table_name + "_table_schema.json"
     with open(table_schema_path) as schema_file:
          json_data = json.load(schema_file)
     table_fields_in_schema = json_data[table_name]
     
     table_fields_in_local_file = local_file_df.columns
     
     equal_field_names_boolean = set(table_fields_in_local_file) == set(local_file_df)
     return equal_field_names_boolean
     
     
def create_parquet_file_and_upload_to_S3(BASE_PATH, table_name, path_to_local_csv_file, partition_id):
     import pandas as pd
     import boto3
     import json
     import pyarrow.parquet as pq
     import pyarrow as pa
     
     local_file_df = pd.read_csv(path_to_local_csv_file)
     path_to_local_parquet_file_with_name = BASE_PATH + '/data_store/data_in_parquet_for_tables/' + table_name + '.parquet.gzip'
     local_file_df.to_parquet(path_to_local_parquet_file_with_name, engine = 'pyarrow', compression = 'gzip')
     
     with open(BASE_PATH + "/credentials/aws_credentials.json") as json_data_file:
          json_data = json.load(json_data_file)
          
     ACCESS_KEY = json_data['Access key ID']
     SECRET_KEY = json_data['Secret access key']
     BUCKET_NAME = json_data['athena_table_bucket']
     s3_file_path_without_bucket = 'data_team/' + table_name + '/' + 'dt=' +  partition_id + '/' + table_name + '_' + partition_id + '.parquet'
     s3_folder_name_for_table = 's3://' + BUCKET_NAME + '/' +  'data_team/' + table_name + '/'
     s3_folder_name_for_file = 's3://' + BUCKET_NAME + '/' + 'data_team/' + table_name + '/' + 'dt=' +  partition_id + '/'
     
     s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
                      
     s3.upload_file(path_to_local_parquet_file_with_name, BUCKET_NAME, s3_file_path_without_bucket)

     
     
     return s3_folder_name_for_table, path_to_local_parquet_file_with_name, s3_folder_name_for_file
     
     
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
     

def create_athena_table(table_name, column_details_string, partition_id, s3_folder_name_for_table):
     from pyathena import connect
          
     cursor = connect(
                 s3_staging_dir="s3://" + BUCKET_NAME,
                 region_name="us-east-1").cursor()
                 
     cursor.execute("""CREATE EXTERNAL TABLE IF NOT EXISTS gold.data_team_{table_name} ({column_details_string})
     PARTITIONED BY (dt varchar(20))
     STORED AS PARQUET
     LOCATION '{s3_folder_name_for_table}'
     TBLPROPERTIES ('parquet.compression'='gzip')
     """.format(
                      table_name = table_name, 
                      column_details_string = column_details_string,
                      partition_id = partition_id, 
                      s3_folder_name_for_table = s3_folder_name_for_table
                 ))
     cursor.close()
            
                 
def alter_athena_table(table_name, partition_id, s3_folder_name_for_file):
     from pyathena import connect
          
     cursor = connect(
                 s3_staging_dir="s3://" + BUCKET_NAME,
                 region_name="us-east-1").cursor()
                 
     cursor.execute("""
     ALTER TABLE gold.data_team_{table_name} 
     ADD PARTITION (dt = {partition_id}) 
     LOCATION '{s3_folder_name_for_file}'
     """.format(
                      table_name = table_name, 
                      partition_id = partition_id, 
                      s3_folder_name_for_file = s3_folder_name_for_file
                 ))
     cursor.close()
     
  
def create_latest_view(table_name, partition_id):
     from pyathena import connect
          
     cursor = connect(
                 s3_staging_dir="s3://" + BUCKET_NAME,
                 region_name="us-east-1").cursor()
                 
     cursor.execute("""
     CREATE OR REPLACE VIEW gold.data_team_{table_name}_latest AS SELECT * FROM gold.data_team_{table_name} WHERE dt = '{partition_id}'
     """.format(
                      table_name = table_name,
                      partition_id = partition_id
                 ))
     cursor.close()
   
   
   
def main_function(BASE_PATH, table_name, path_to_local_csv_file):
     from datetime import datetime
     import sys
     import importlib
     import json
     
     global BUCKET_NAME
     #BASE_PATH = '/home/luis/Zemee College_data_project/etl_code/data_team_etl'
     
     with open(BASE_PATH + "/credentials/aws_credentials.json") as json_data_file:
          json_data = json.load(json_data_file)
          
     BUCKET_NAME = json_data['athena_table_bucket']
     
     print("\n\n\tBegin Athena table updates")
     current_datetime = datetime.now()
     equal_field_names_boolean = verify_table_fields_with_config(BASE_PATH, table_name, path_to_local_csv_file)
     if equal_field_names_boolean != True:
          print("Table not updated as field verification failed. fields_in_created_csv != fields_in_config_file")
     else:
          partition_id = current_datetime.strftime('%Y') + current_datetime.strftime('%m') + current_datetime.strftime('%d') + current_datetime.strftime('%H') + current_datetime.strftime('%M') + current_datetime.strftime('%S')
          print('partition_id:', partition_id)
          s3_folder_name_for_table, path_to_local_parquet_file_with_name, s3_folder_name_for_file = create_parquet_file_and_upload_to_S3(BASE_PATH, table_name, path_to_local_csv_file, partition_id)
          print("Parquet file created and uploaded to S3")
          column_details_string = create_table_column_details(path_to_local_parquet_file_with_name)
          create_athena_table(table_name, column_details_string, partition_id, s3_folder_name_for_table)
          print("Athena table created if didn't exist")
          alter_athena_table(table_name, partition_id, s3_folder_name_for_file)
          print("Athena table altered to update new data")
          create_latest_view(table_name, partition_id)
          print("Latest view created for the table")
          
          slack_text = "Athena table updated for {table_name} for {file_name}".format(table_name= table_name, file_name= path_to_local_csv_file.split("/")[-1])
          print(slack_text)
          
          sys.path.insert(0,BASE_PATH + '/helper_functions/')
          import send_slack_notifications
          importlib.reload(send_slack_notifications)
          send_slack_notifications.send_message_to_slack(slack_text, slack_channel = 'data-reports')

if __name__ == '__main__':
     table_name = 'one_pager_data_part2_by_gender'
     path_to_local_csv_file = '/home/luis/Zemee College_data_project/data-team/data_team_etl/data_store/data_in_csv_for_tables/{table_name}_FallFirst_time.csv'.format(table_name = table_name)
     BASE_PATH = "/home/luis/Zemee College_data_project/data-team/data_team_etl"
     main_function(BASE_PATH, table_name, path_to_local_csv_file)
     



                 
                 
