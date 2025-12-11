"""
Gmail Reader - Fetch and summarize emails using Gmail API
"""

import os
import pickle
import base64
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
import sys

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    logger.warning("Gmail API libraries not installed")

# Configure logger
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("logs/gmail_reader.log", rotation="10 MB")

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailReader:
    """Gmail email fetching and summarization"""
    
    def __init__(
        self,
        credentials_path: str = "credentials.json",
        token_path: str = "token.pickle"
    ):
        """
        Initialize Gmail reader
        
        Args:
            credentials_path: Path to OAuth credentials JSON
            token_path: Path to store authentication token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API using OAuth"""
        creds = None
        
        # Check for existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing expired token")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    logger.error(f"Credentials file not found: {self.credentials_path}")
                    logger.info("Please download OAuth credentials from Google Cloud Console")
                    return
                
                logger.info("Starting OAuth flow - browser will open")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
            
            logger.info("Authentication successful")
        
        # Build Gmail service
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail service initialized")
        except Exception as e:
            logger.error(f"Failed to build Gmail service: {e}")
    
    def fetch_emails(
        self,
        query: str = "is:unread",
        max_results: int = 10,
        include_body: bool = True
    ) -> Dict[str, any]:
        """
        Fetch emails matching query
        
        Args:
            query: Gmail search query (e.g., "is:unread", "from:example@gmail.com")
            max_results: Maximum number of emails to fetch
            include_body: Whether to fetch full email body
            
        Returns:
            Dict with emails and metadata
        """
        if not self.service:
            logger.error("Gmail service not initialized")
            return {"emails": [], "error": "Not authenticated", "count": 0}
        
        try:
            # Search for messages
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                logger.info("No messages found")
                return {"emails": [], "error": None, "count": 0}
            
            # Fetch full message details
            emails = []
            for msg in messages:
                email_data = self._get_message_details(msg['id'], include_body)
                if email_data:
                    emails.append(email_data)
            
            logger.info(f"Fetched {len(emails)} emails")
            
            return {
                "emails": emails,
                "error": None,
                "count": len(emails)
            }
        
        except HttpError as error:
            logger.error(f"Gmail API error: {error}")
            return {"emails": [], "error": str(error), "count": 0}
    
    def _get_message_details(self, msg_id: str, include_body: bool) -> Optional[Dict]:
        """Get full details of a single message"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            # Extract headers
            headers = message['payload']['headers']
            subject = self._get_header(headers, 'Subject')
            sender = self._get_header(headers, 'From')
            date = self._get_header(headers, 'Date')
            
            # Extract body if requested
            body = ""
            if include_body:
                body = self._get_message_body(message)
            
            return {
                "id": msg_id,
                "subject": subject,
                "from": sender,
                "date": date,
                "snippet": message.get('snippet', ''),
                "body": body
            }
        
        except Exception as e:
            logger.error(f"Error fetching message {msg_id}: {e}")
            return None
    
    def _get_header(self, headers: List[Dict], name: str) -> str:
        """Extract specific header value"""
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ""
    
    def _get_message_body(self, message: Dict) -> str:
        """Extract email body text"""
        try:
            # Try to get plain text body
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data', '')
                        if data:
                            return base64.urlsafe_b64decode(data).decode('utf-8')
            
            # If no parts, try direct body
            if 'body' in message['payload'] and 'data' in message['payload']['body']:
                data = message['payload']['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
            
            return ""
        
        except Exception as e:
            logger.warning(f"Error decoding message body: {e}")
            return ""
    
    def summarize_emails(self, emails: List[Dict], llm_chat) -> str:
        """
        Summarize a list of emails using LLM
        
        Args:
            emails: List of email dicts
            llm_chat: LLMChat instance
            
        Returns:
            Summarized text
        """
        if not emails:
            return "No emails to summarize."
        
        # Format emails for LLM
        email_texts = []
        for email in emails:
            email_text = f"""
From: {email['from']}
Subject: {email['subject']}
Date: {email['date']}
Preview: {email['snippet']}
"""
            email_texts.append(email_text)
        
        combined = "\n---\n".join(email_texts)
        
        system_prompt = f"""Summarize these {len(emails)} emails concisely.
For each email, provide:
- Sender
- Subject
- Brief summary (1-2 sentences)

Format as a bulleted list."""
        
        summary = llm_chat.generate_response(
            combined,
            system_prompt=system_prompt,
            temperature=0.3
        )
        
        return summary
    
    def get_unread_count(self) -> int:
        """Get count of unread emails"""
        if not self.service:
            return 0
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=1
            ).execute()
            
            return results.get('resultSizeEstimate', 0)
        except Exception as e:
            logger.error(f"Error getting unread count: {e}")
            return 0
