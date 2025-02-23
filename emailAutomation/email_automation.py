import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

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
        dicto = {
            "type":"text",
            "data":"Email sent successfully!"
        }
        return dicto
    except Exception as e:

        dicto = {
            "type": "text",
            "data": "Email Failed!"
        }
        print("Error:", e)
        return dicto
        

def read_emails(number_of_emails=5, unread_only=True):
    """
    Read emails from the inbox.

    Parameters
    ----------
    number_of_emails : int, optional
        Number of recent emails to fetch (default is 5)
    unread_only : bool, optional
        If True, fetch only unread emails (default is True)

    Returns
    -------
    dict
        Dictionary containing email data
    """
    load_dotenv()
    email_password = os.getenv("EMAIL_PASSWORD")
    email_address = "team.event.horizon.iiitp@gmail.com"

    try:
        # Connect to Gmail's IMAP server
        imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
        imap_server.login(email_address, email_password)
        
        # Select the inbox
        imap_server.select("INBOX")

        # Search for unread emails if unread_only is True, otherwise get all emails
        search_criterion = '(UNSEEN)' if unread_only else 'ALL'
        _, message_numbers = imap_server.search(None, search_criterion)
        email_ids = message_numbers[0].split()
        
        # Get the last n email IDs
        latest_email_ids = email_ids[-number_of_emails:] if email_ids else []

        emails_data = []
        for email_id in latest_email_ids:
            _, msg_data = imap_server.fetch(email_id, "(RFC822)")
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)

            # Extract email content
            content = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        content = part.get_payload(decode=True).decode()
                        break
            else:
                content = email_message.get_payload(decode=True).decode()

            # Extract email information
            subject = email_message["subject"]
            from_address = email_message["from"]
            date = email_message["date"]

            emails_data.append({
                "from": from_address,
                "subject": subject,
                "date": date,
                "content": content
            })

        imap_server.close()
        imap_server.logout()

        return {
            "type": "text",
            "data": emails_data
        }

    except Exception as e:
        print("Error:", e)
        return {
            "type": "text",
            "data": [f"Error reading emails: {str(e)}"]
        }

if __name__ == "__main__":
    print(send_email("siddhantganesh25@gmail.com", "HELLO", "HELLO"))