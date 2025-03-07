import datetime
from bson import ObjectId
from pymongoose import methods
from jinja2 import Environment, FileSystemLoader
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv


from ..modules.messages import  EmailStatus
from ..constants.email_constants import EmailConstants 


class EmailService:
    

    def send_email(self, model: dict):
        load_dotenv()
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")

        

    
        if not sender_email or not sender_password:
            return EmailStatus.error_missing_credentials()
        try:
            
          

            env = Environment(loader=FileSystemLoader('chalicelib'))
            template = env.get_template('invitation_template.html')
            html_content = template.render(
                    project_name=model.get("projectName"),
                    id=model.get("invitationId"),
                    link=model.get("linkInvitation"),
                    logo_path=EmailConstants.LOGO_PATH,
                    greeting=EmailConstants.GREETING,
                    invitation_header=EmailConstants.INVITATION_HEADER,
                    invitation_body=EmailConstants.INVITATION_BODY,
                    accept_invitation=EmailConstants.ACCEPT_INVITATION,
                    button_text=EmailConstants.BUTTON_TEXT,
                    footer_text=EmailConstants.FOOTER_TEXT,
                    ignore_message=EmailConstants.IGNORE_MESSAGE
            )

            
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = model["receiverEmail"]
            msg["Subject"] = model["subject"]
            msg.attach(MIMEText(html_content, "html"))

           
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, model["receiverEmail"], msg.as_string())
            server.quit()

            
            return EmailStatus.success()

        except Exception as e:
           
            return EmailStatus.error_sending_failed(str(e))
