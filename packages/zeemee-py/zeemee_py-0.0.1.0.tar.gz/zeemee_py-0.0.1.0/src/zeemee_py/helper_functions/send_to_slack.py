
def send_message_to_slack(channel_name, text ):
     from urllib import request
     import json
     from zeemee_py.helper_functions import get_config
     
     post = {"text": "{0}".format(text)}
     
     if channel_name == "data-reports":
          slack_url = get_config.get_creds("slackurl_data_reports")
     elif channel_name == "full-pipeline-logs":
          slack_url = get_config.get_creds("slackurl_full_pipeline_logs")
     elif channel_name == "comms":
          slack_url = get_config.get_creds("slackurl_comms")
     else:
          slack_url = get_config.get_creds("slackurl_data_reports") #we keep data-team channel as the default slack channel
     
     try:
          json_data = json.dumps(post)
          req = request.Request(
               slack_url,
               data= json_data.encode("ascii"),
               headers={"Content-Type": "application/json"}
               ) 
          resp = request.urlopen(req)
     
     except Exception as em:
          print("EXCEPTION: " + str(em))

