
def upload_engagement_data_to_admin(organization_id, organization_slug, s3_file_path):
     import importlib
     import time
     
     s3_file_name = s3_file_path.split("/")[-1]
     
     from zeemee_py.helper_functions import send_to_admin_and_make_visible
     importlib.reload(send_to_admin_and_make_visible)
     send_to_admin_and_make_visible.send_to_admin_and_make_visible(organization_id, s3_file_name)
     
     slack_message = "Touchpoints for {organization_slug} uploaded to admin".format(organization_slug = organization_slug)
     print(slack_message)
     
     from zeemee_py.helper_functions import send_to_slack
     importlib.reload(send_to_slack)
     send_to_slack.send_message_to_slack( "data-reports", slack_message)
     
     time.sleep(1)
