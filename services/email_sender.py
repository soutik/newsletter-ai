import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_email(receiver_email, html_content, smtp_server="smtp.gmail.com", smtp_port=587):
    try:
        sender_email = os.getenv("SENDER_EMAIL", "someone@gmail.com")
        sender_password = os.getenv("SENDER_PASSWORD", "password")

        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = sender_password
        msg["Subject"] = "Your daily newsletter!"

        # Attach the HTML content
        msg.attach(MIMEText(html_content, "html"))

        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure connection
        server.login(sender_email, sender_password)  # Login to email account

        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Close connection
        server.quit()
        print(f"Email sent successfully to {receiver_email}")
    
    except Exception as e:
        print(f"Error sending email: {e}")