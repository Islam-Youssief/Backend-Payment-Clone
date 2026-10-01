import api.core.configurations as config
import smtplib

from email.message import EmailMessage

class EmailService:

    @staticmethod
    def send_password_reset_otp(received_email,otp):
        smtp_host = config.SmtpConfig.smtp_host
        smtp_port = config.SmtpConfig.smtp_port
        smtp_username = config.SmtpConfig.smtp_username
        smtp_password = config.SmtpConfig.smtp_password
        smtp_from = config.SmtpConfig.smtp_from

        message = EmailMessage()

        message["Subject"] = "Password Reset OTP"
        message["From"] = smtp_from
        message["To"] = received_email

        message.set_content(f"""
        Email Verification Code
        Enter this code on the identity verification screen:
        {otp}
        This code will expire shortly.""")

        with smtplib.SMTP(smtp_host,int(smtp_port)) as smtp:
            smtp.starttls()

            smtp.login(smtp_username,smtp_password)

            smtp.send_message(message)