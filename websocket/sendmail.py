# import os
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from websocket.settings import *
# from django.template.loader import render_to_string
# from bs4 import BeautifulSoup

# def send_email(subject, to_email):
#     from_email = EMAIL_HOST_USER
#     from_email_password = EMAIL_HOST_PASSWORD

#     # Create the message
#     msg = MIMEMultipart()
#     msg['From'] = from_email
#     msg['To'] = to_email
#     msg['Subject'] = subject

#     # Load the HTML template
#     html_body = render_to_string("email.html")

#     # Parse the HTML and extract text content
#     soup = BeautifulSoup(html_body, "html.parser")
#     text_content = soup.get_text()

#     # Attach the text content of the email
#     msg.attach(MIMEText(text_content, 'plain'))

#     try:
#         # Set up the server
#         server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
#         server.starttls()  # Use TLS

#         # Log in to the server
#         server.login(from_email, from_email_password)

#         # Send the email
#         server.send_message(msg)

#         # Disconnect from the server
#         server.quit()

#         print("Email sent successfully!")

#     except Exception as e:
#         print(f"Failed to send email. Error: {e}")

# # Example usage:
# # send_email("Subject", "recipient@example.com")


# myapp/utils.py

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_test_email(recipient_email, context):
    subject = 'Welcome to Nexby AI Interview Tool'
    message = render_to_string('email.html', context)
    
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [recipient_email],
    )
    email.content_subtype = 'html'  # Main content is now text/html
    try:
        email.send()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
