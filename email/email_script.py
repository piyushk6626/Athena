import smtplib
import openai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# OpenAI API Key
openai.api_key ="openAi_api_key"
# Function to generate email content
def generate_email(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Function to send email
def send_email(sender_email, sender_password, recipient_email, subject, body):
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
        print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)

# User Input
recipient_email = "reciver_email"
email_subject = "Generated Email"
email_prompt = input("Enter prompt for OpenAI to generate email: ")

# Generate and send email
email_body = generate_email(email_prompt)
send_email("dev.forge06@gmail.com", "app_password", recipient_email, email_subject, email_body)