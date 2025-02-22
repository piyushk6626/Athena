import smtplib
import openai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# OpenAI API Key

# Function to send emaile
def send_email(recipient_email, subject, body):
    
    """
    Send an email to the given recipient with the given subject and body.

    Parameters
    ----------
    recipient_email : str
        The email address of the recipient.
    subject : str
        The subject of the email.
    body : str
        The contents of the email.

    Raises
    ------
    Exception
        If there is any error while sending the email.
    """
    sender_password = "mdrn blsj vrhy mpwc"
    sender_email = "soulmortal309@gmail.com"
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