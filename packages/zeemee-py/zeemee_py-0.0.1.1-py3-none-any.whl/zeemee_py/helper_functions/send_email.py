#recipient_list = ['mayur@zeemee.com', 'mayur@zeemee.com']

def send_email(recipient_list, subject_text, message_text):
     import importlib
     import smtplib
     import time
     
     from zeemee_py.helper_functions import get_config
     emailhostname, emailusername, emailpwd = get_config.get_creds("emailhostname", "emailusername", "emailpwd")
     
     message_text = "Subject: {subject_text}\n\n{message_text}".format(
          subject_text = subject_text, 
          message_text = message_text
          )
     
     import smtplib
     server = smtplib.SMTP(emailhostname)
     server.starttls()
     server.login(emailusername, emailpwd)
     server.sendmail(emailusername, recipient_list, message_text)
     server.quit()
     time.sleep(1)
     
     print("email sent to " + ", ".join(recipient_list))

