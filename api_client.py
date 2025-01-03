import requests
import logging
from datetime import datetime


# TODO: Implement custom error handling
# class APIClientError(Exception):
#     """Custom exception for API client errors"""
#     pass


class MessageAPIClient():

    def __init__(self, bot_id, base_url, logger=None):
        """
        Initialize API client
        
        Args:
            base_url: Base URL of the API server (e.g., 'http://api.example.com')
            bot_id: Unique identifier for this bot
        """
        self.base_url = base_url.rstrip('/')
        self.bot_id = bot_id
        if not logger:
            logger = logging.getLogger(__name__)
        self.logger = logger


    def get_messages(self, state, limit=2) -> list:
        """
        Get messages, optionally filtered by user
        
        Args:
            user_id: Optional Telegram user ID to filter by
            limit: Maximum number of messages to return
            
        Returns:
            List of message dictionaries
        """
        params = {
            'bot_id': self.bot_id,
            'limit': limit
        }
        if state:
            params['state'] = state
            
        response = self._make_request(
            method='GET',
            endpoint='/api/v1/messages',
            params=params
        )

        return response.get('messages', [])


    def store_message(self, state, text) -> dict:
        """
        Store a new message
        
        Args:
            user_id: Telegram user ID
            text: Message text
            reply_to: Optional ID of message being replied to
            
        Returns:
            Response from API server
        """
        payload = {
            "bot_id": self.bot_id,
            'message': {
                "state": state,
                "text": text,
                "timestamp": datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            }
        }

        return self._make_request(
            method='POST',
            endpoint='/api/v1/messages',
            json=payload
        )


    def _make_request(self, method, endpoint, **kwargs) -> dict:
        """
        Make HTTP request to API server
        
        Args:
            method: HTTP method ('GET', 'POST', etc.)
            endpoint: API endpoint (will be appended to base_url)
            **kwargs: Additional arguments to pass to requests
        
        Returns:
            Response JSON
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                # headers=self.headers,
                **kwargs
            )
            
            # Raise error for bad status codes
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            raise Exception(f"API request failed: {str(e)}")
        except ValueError as e:
            self.logger.error(f"Invalid JSON response: {str(e)}")
            raise Exception(f"Invalid JSON response: {str(e)}")
