"""
This script is used to send messages to "data-reports" slack channel
errors are logged in slack_fail_logs.log file with channel name

to use this script:

sys.path.insert(0,BASE_PATH + '/helper_functions/')
import send_slack_notifications
importlib.reload(send_slack_notifications)
send_slack_notifications.send_message_to_slack(text, slack_channel, format_to_code_block)

"""

def send_message_to_slack(text, slack_channel, format_to_code_block = "yes"):
     import requests
     import json
     
     if format_to_code_block == "yes":
          text = "```" + text + "```" #to format as a code block
          
     json_text = {
          "type": "mrkdwn",
          "text":  text
          }

     try:
          BASE_PATH = "/home/luis/Zemee College_data_project/data-team/data_team_etl"
          
          path_to_slack_channel_file = BASE_PATH + "/credentials/slack_channels.json"
          with open(path_to_slack_channel_file) as json_data_file:
               slack_channel_data = json.load(json_data_file)
          channel_url = slack_channel_data[slack_channel]
          
          x = requests.post(
               channel_url,
               json = json_text,
               headers={'Content-Type': 'application/json'}
               )
          if x.status_code == 200:
             print("Text sent to {slack_channel} channel".format(slack_channel= slack_channel))
          else:
               print("Failed to send text to {slack_channel} channel. Status ".format(slack_channel = slack_channel) + str(x.status_code))
     except:
          print("Error in send_slack_notification_code")

if __name__ == "__main__":
     text = "test message to check formatting"
     send_message_to_slack(text, "data-reports")
