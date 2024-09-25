import os
from dotenv import load_dotenv
from trycourier import Courier

load_dotenv()

client = Courier(auth_token=os.getenv('COURIER_TOKEN'))

def send_email_verification(email:str, first_name:str, link:str):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": os.getenv('EMAIL_VERIFICATION_TEMPLATE_ID'),
            "data": {
            "firstName": first_name,
            "link": link,
            },
        }
    )
