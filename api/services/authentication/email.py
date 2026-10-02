import api.core.configurations as config
import smtplib

from email.message import EmailMessage

class EmailService:
    def __init__(self):
        self.smtp_host = config.SmtpConfig.smtp_host
        self.smtp_port = config.SmtpConfig.smtp_port
        self.smtp_username = config.SmtpConfig.smtp_username
        self.smtp_password = config.SmtpConfig.smtp_password
        self.smtp_from = config.SmtpConfig.smtp_from

    def send_password_reset_otp(self,received_email,otp):

        message = EmailMessage()

        message["Subject"] = "Password Reset OTP"
        message["From"] = self.smtp_from
        message["To"] = received_email

        message.set_content(f"""
        Email Verification Code
        Enter this code on the identity verification screen:
        {otp}
        This code will expire shortly.""")

        with smtplib.SMTP(self.smtp_host,int(self.smtp_port)) as smtp:
            smtp.starttls()

            smtp.login(self.smtp_username,self.smtp_password)

            smtp.send_message(message)

    def send_error(self,email,error_level,exception_name,traceback_text):
        message = EmailMessage()
        message["Subject"] = f"Error level : {error_level} - {exception_name}"
        message["From"] = self.smtp_from
        message["To"] = email

        message.set_content(f"{exception_name}.\n{traceback_text}""")

        with smtplib.SMTP(self.smtp_host,int(self.smtp_port)) as smtp:
            smtp.starttls()

            smtp.login(self.smtp_username,self.smtp_password)

            smtp.send_message(message)