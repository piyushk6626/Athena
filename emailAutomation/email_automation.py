import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables once at module level
load_dotenv()

# Constants
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
IMAP_SERVER = 'imap.gmail.com'
DEFAULT_EMAIL = "team.event.horizon.iiitp@gmail.com"

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

    Returns
    -------
    dict
        Dictionary with status information about the email operation.

    Raises
    ------
    Exception
        If there is any error while sending the email.
    """
    # Get credentials from environment variables
    sender_password = os.getenv("EMAIL_PASSWORD")
    sender_email = DEFAULT_EMAIL
    
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable TLS encryption
        
        # Login and send the email
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        # Return success status
        return {
            "type": "text",
            "data": "Email sent successfully!"
        }
    except Exception as e:
        # Handle errors and return failure status
        print("Error:", e)
        return {
            "type": "text",
            "data": "Email Failed!"
        }
        

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
    # Get credentials from environment variables
    email_password = os.getenv("EMAIL_PASSWORD")
    email_address = DEFAULT_EMAIL

    try:
        # Connect to Gmail's IMAP server
        imap_server = imaplib.IMAP4_SSL(IMAP_SERVER)
        imap_server.login(email_address, email_password)
        
        # Select the inbox
        imap_server.select("INBOX")

        # Search for unread emails if unread_only is True, otherwise get all emails
        search_criterion = '(UNSEEN)' if unread_only else 'ALL'
        _, message_numbers = imap_server.search(None, search_criterion)
        email_ids = message_numbers[0].split()
        
        # Get the last n email IDs
        latest_email_ids = email_ids[-number_of_emails:] if email_ids else []

        # Process each email
        emails_data = []
        for email_id in latest_email_ids:
            # Fetch email data
            _, msg_data = imap_server.fetch(email_id, "(RFC822)")
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)

            # Extract email content
            content = _extract_email_content(email_message)

            # Extract email metadata
            subject = email_message["subject"]
            from_address = email_message["from"]
            date = email_message["date"]

            # Add email to results
            emails_data.append({
                "from": from_address,
                "subject": subject,
                "date": date,
                "content": content
            })

        # Close connection
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

def _extract_email_content(email_message):
    """
    Helper function to extract content from email message.
    
    Parameters
    ----------
    email_message : email.message.Message
        The email message object to extract content from
        
    Returns
    -------
    str
        The plain text content of the email
    """
    content = ""
    if email_message.is_multipart():
        # If email has multiple parts, find the text/plain part
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                content = part.get_payload(decode=True).decode()
                break
    else:
        # If email is not multipart, just get the payload
        content = email_message.get_payload(decode=True).decode()
    
    return content

if __name__ == "__main__":
    # Example usage
    print(send_email("siddhantganesh25@gmail.com", "HELLO", "HELLO"))