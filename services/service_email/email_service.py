import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from core.LogManager import log


class EmailService:

    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.email = os.getenv("SMTP_EMAIL")
        self.password = os.getenv("SMTP_PASSWORD")


    def send_otp(self, email: str, otp: str):

        subject = "Your Login OTP"

        body = f"""
Hello,

Your OTP is:

{otp}

This OTP will expire in 5 minutes.

If you didn't request this OTP, please ignore this email.

Regards,
Leetcode Tutor
"""

        try:

            message = MIMEMultipart()

            message["From"] = self.email
            message["To"] = email
            message["Subject"] = subject

            message.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP(
                self.smtp_host,
                self.smtp_port
            )

            server.starttls()

            server.login(
                self.email,
                self.password
            )

            server.sendmail(
                self.email,
                email,
                message.as_string()
            )

            server.quit()

            log.info(f"OTP sent successfully -> {email}")

            return {
                "status": 200,
                "message": "Email sent successfully"
            }

        except Exception as EmailException:

            log.exception(
                f"Email send failed | {EmailException}"
            )

            return {
                "status": 500,
                "message": "Failed to send email"
            }


email_service = EmailService()