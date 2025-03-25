"""
Email Automation Package
=======================

A simple yet powerful email automation package for sending and reading emails using Gmail.

This package provides functionality to:
    - Send emails using Gmail's SMTP server
    - Read emails from Gmail inbox (both unread and all emails)
    - Handle email attachments and multipart messages

Main Functions:
--------------
    send_email(recipient_email, subject, body):
        Send an email to a specified recipient with given subject and body.
    
    read_emails(number_of_emails=5, unread_only=True):
        Read specified number of emails from the Gmail inbox.

Usage Example:
-------------
    from emailAutomation import send_email, read_emails
    
    # Send an email
    send_email("recipient@example.com", "Hello", "This is a test email")
    
    # Read last 5 unread emails
    emails = read_emails(number_of_emails=5, unread_only=True)

Note:
-----
    Requires Gmail credentials to be set in environment variables:
    - EMAIL_PASSWORD: Your Gmail app password
"""

from .email_automation import send_email, read_emails

__all__ = [
    'send_email',
    'read_emails'
]

# Version of the email automation package
__version__ = '0.1.0'
