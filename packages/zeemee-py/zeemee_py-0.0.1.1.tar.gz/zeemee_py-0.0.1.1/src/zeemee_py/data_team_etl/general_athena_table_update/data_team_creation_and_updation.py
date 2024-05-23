
import pandas as pd
table_name = "zm_status_translations"
original_file = "/home/luis/Zeemee Client_data/rawCollegeFiles/ZM Status Translations.xlsx"
data_df = pd.read_excel(original_file)


"""
How to use this function:
Table creation notes:
1. This function creates only data_team tables

2. Clean all the field names before passing the dataframe to this funtion 
     - make lower case
     - replace '.' with '_'
     - replace ' ' with '_' 
     - replace '-' with '_'
     
     Example code, adjust as needed:
          
          -----------
          new_column_values = list()
          data_frame_columns = data_df.columns
          
          for i in data_df.columns:
               new_value = i.lower()
               new_value = new_value.replace(".","_")
               new_value = new_value.replace(" ","_")
               new_value = new_value.replace("-","_")
               new_column_values.append(new_value)

          for i in range(len(data_frame_columns)):
               data_df.rename(columns = {data_frame_columns[i]:new_column_values[i]}, inplace = True) 
          -----------
     
     
Table Updation notes:
1. This function replaces existing data with the dataframe. So any updation/ deletion to the table must
     be done before passing the dataframe and table name to this function  

2. data_df: this is the dataframe of the table to be created

3. table_name: name of the table like all_partner_data. DO NOT add data_team prefix to the value!

"""

def create_or_update_athena_data_team_table(data_df, table_name):
     print("Table creation function started")
     
     import pandas as pd
     import datetime
     import json
     import pyarrow as pa
     import pyarrow.parquet as pq
     import boto3
     from pyathena import connect
     import sys
     import importlib
          
     BASE_PATH = "/home/luis/Zemee College_data_project/data-team/data_team_etl"
     
     #path_to_local_csv_file_with_name =  BASE_PATH + "/general_athena_table_update/parquet_file_for_update/" + table_name + ".csv"
     path_to_local_parquet_file_with_name = BASE_PATH + "/general_athena_table_update/parquet_file_for_update/" + table_name + ".gzip"
     data_df.to_parquet(path_to_local_parquet_file_with_name, engine = 'pyarrow', compression = 'gzip')
     
     today_date = datetime.datetime.today().strftime('%Y-%m-%d')
     today_day = datetime.datetime.today().strftime('%A') 
     current_datetime = datetime.datetime.today()
     partition_id = current_datetime.strftime('%Y') + current_datetime.strftime('%m') + current_datetime.strftime('%d') + current_datetime.strftime('%H') + current_datetime.strftime('%M') + current_datetime.strftime('%S')
     
     
     with open(BASE_PATH + "/credentials/aws_credentials.json") as json_data_file:
               json_data = json.load(json_data_file)
               
     ACCESS_KEY = json_data['Access key ID']
     SECRET_KEY = json_data['Secret access key']
     BUCKET_NAME = json_data['athena_table_bucket']
     
     s3_file_path_without_bucket = 'data_team/' + table_name + '/' + 'dt=' +  partition_id + '/' + 'data_team_' + table_name + '_' + partition_id + '.parquet'
     s3_folder_name_for_table = 's3://' + 'prod-zeemee-data-lake' + '/' +  'data_team/' + table_name + '/'
     s3_folder_name_for_file = 's3://' + 'prod-zeemee-data-lake' + '/' + 'data_team/' + table_name + '/' + 'dt=' +  partition_id + '/'
     
     s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
     s3.upload_file(path_to_local_parquet_file_with_name, BUCKET_NAME, s3_file_path_without_bucket)
     print("____ Parquet file uploaded to S3")
          
     
     cursor = connect(
                 s3_staging_dir="s3://" + BUCKET_NAME,
                 region_name="us-east-1").cursor()
                 
     sys.path.insert(0,BASE_PATH + '/general_athena_table_update/')
     import get_column_details
     importlib.reload(get_column_details)
     column_details_string = get_column_details.create_table_column_details(path_to_local_parquet_file_with_name)
     
     
     cursor.execute("""CREATE EXTERNAL TABLE IF NOT EXISTS gold.data_team_{table_name} (
          {column_details_string}
          )
          PARTITIONED BY (dt varchar(20))
          STORED AS PARQUET
          LOCATION '{s3_folder_name_for_table}'
          TBLPROPERTIES ('parquet.compression'='gzip')
     """.format(
          table_name = table_name, 
          column_details_string = column_details_string,
          s3_folder_name_for_table = s3_folder_name_for_table,
          )
          )
     cursor.close()
     print("____ Table created if didn't exist")
     
     
     cursor = connect(
                 s3_staging_dir="s3://" + BUCKET_NAME,
                 region_name="us-east-1").cursor()
                 
     cursor.execute("""ALTER TABLE gold.data_team_{table_name}
          ADD PARTITION (dt = {partition_id}) 
          LOCATION '{s3_folder_name_for_file}'
     """.format(
          table_name = table_name,
          partition_id = partition_id,
          s3_folder_name_for_file = s3_folder_name_for_file
          )
          )
     cursor.close()
     print("____ Alter table completed")
     
     
     cursor = connect(
                 s3_staging_dir="s3://" + BUCKET_NAME,
                 region_name="us-east-1").cursor()
                      
     cursor.execute("""
     CREATE OR REPLACE VIEW gold.data_team_{table_name}_latest 
     AS SELECT * FROM gold.data_team_{table_name} 
     WHERE dt = '{partition_id}'
     """.format(
          table_name = table_name,
          partition_id = partition_id
                 ))
     cursor.close()
     print("____ Latest view created")
     print("Table creation function complete")

