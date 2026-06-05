#!/usr/bin/env python3
"""
Email notification service
"""

import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailService:
    """Sends email notifications"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.notification_email = os.getenv('NOTIFICATION_EMAIL')
    
    def send_application_email(self, job):
        """Send email notification for job application"""
        
        if not self.sender_email or not self.sender_password:
            logger.warning("Email credentials not configured.")
            return False
        
        try:
            subject = f"Applied to {job.get('title', 'N/A')} at {job.get('company', 'N/A')}"
            body = f"You have applied to {job.get('title')} at {job.get('company')}"
            
            return self._send_email(subject, body, self.notification_email or self.sender_email)
        
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_summary_email(self, summary):
        """Send summary email"""
        
        if not self.sender_email or not self.sender_password:
            logger.warning("Email credentials not configured.")
            return False
        
        try:
            subject = f"Job Application Agent Summary - {datetime.now().strftime('%Y-%m-%d')}"
            
            return self._send_email(subject, summary, self.notification_email or self.sender_email)
        
        except Exception as e:
            logger.error(f"Error sending summary: {str(e)}")
            return False
    
    def _send_email(self, subject, body, recipient):
        """Send email via SMTP"""
        
        try:
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = recipient
            
            text_part = MIMEText(body, 'plain')
            message.attach(text_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logger.info(f"Email sent to {recipient}")
            return True
        
        except Exception as e:
            logger.error(f"SMTP error: {str(e)}")
            return False