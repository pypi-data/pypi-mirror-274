
def upload_to_s3(local_file, bucket_name, s3_file_name):
     import boto3
     from botocore.exceptions import NoCredentialsError
     from zeemee_py.helper_functions import get_config
     
     accesskeyid, accesskey = get_config.get_creds("accesskeyid", "accesskey")
     
     s3 = boto3.client(
          "s3", 
          aws_access_key_id=accesskeyid, 
          aws_secret_access_key=accesskey
          )
     
     try:
          s3.upload_file(local_file, bucket_name, s3_file_name)
          print("Uploading to S3 bucket successful")
          return True
     except FileNotFoundError:
          print("The file was not found while uploading to S3")
          return False
     except NoCredentialsError:
          print("Credentials not available while uploading to S3")
          return False

