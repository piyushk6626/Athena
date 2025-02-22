import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Function to send emaile
def send_email(recipient_email, subject, body):
 
    """
    Send an email to the given recipient with the given subject and body.

    Args:
    recipient_email (str): The email address of the recipient.
    subject (str): The subject of the email.
    body (str): The contents of the email.

    Returns:
    dict: A dictionary with the following keys:
        - type (str): The type of response, which is "text".
        - data (list): A list containing a success message if the email is sent successfully.
    """
    load_dotenv()
    sender_password = os.getenv("EMAIL_PASSWORD")
    sender_email = "team.event.horizon.iiitp@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return{
            "type":"text",
            "data":["Email sent successfully!"]
        }
    except Exception as e:
        print("Error:", e)

# # User Input
# recipient_email = "reciver_email"
# email_subject = "Generated Email"
# email_prompt = input("Enter prompt for OpenAI to generate email: ")

# Generate and send email
# send_email('siddhantganesh25@gmail.com', 'Generated Email', 'Hello')
if __name__ == "__main__":
    send_email("kulkarnipiyush462@gmail.com","hi","hi piyush the grate")