import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_USER = os.getenv("EMAIL_USER")
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class EmailService:

    @staticmethod
    def send_email(message, subject, recipient):

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = recipient

        msg.set_content(message)
        if not EMAIL_USER or not EMAIL_PASSWORD:
            raise ValueError("Email credentials not configured")
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
              smtp.login(EMAIL_USER, EMAIL_PASSWORD)
              smtp.send_message(msg)
        

              logger.info("Email sent successfully")   
              return True 
        except Exception  :
               logger.error("Failed to send email", exc_info=True)
             
               return False 


if __name__ == "__main__":
    if __name__ == "__main__":
        EmailService.send_email(
            message="Website is down",
            subject="Monitor Alert",
            recipient="youremail@email.com"
        )
    