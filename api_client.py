import os
import base64
import requests
import time
from typing import Optional, List, Dict, Any

class ClaudeAPIClient:
    """
    Client for interacting with Anthropic's Claude API, supporting both text and image inputs.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    
    def encode_image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def create_message(
        self,
        text_prompt: str,
        image_paths: Optional[List[str]] = None,
        model: str = "claude-3-7-sonnet-20250219",
        max_tokens: int = 1024,
        temperature: float = 0.7,
        status_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        # Create the content array with the text prompt
        content = [{"type": "text", "text": text_prompt}]
        
        # Add images if provided
        if image_paths:
            for image_path in image_paths:
                # Get image media type based on file extension
                media_type = self._get_media_type(image_path)
                
                # Add the base64-encoded image to the content array
                image_base64 = self.encode_image_to_base64(image_path)
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_base64
                    }
                })
        
        # Prepare the request payload
        payload = {
            "model": "claude-3-7-sonnet-20250219",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ]
        }
        
        # Send the request with retries
        max_retries = 3
        retry_delay = 1  # Start with 1 second delay
        last_error = None
        
        for attempt in range(max_retries):
                try:
                    response = requests.post(
                        self.base_url,
                        headers=self.headers,
                        json=payload,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        return response.json()
                    else:
                        error_message = f"API Error: {response.status_code} - {response.text}"
                        if status_callback:
                            status_callback(error_message)
                        raise requests.exceptions.RequestException(error_message)
                        
                except requests.exceptions.RequestException as e:
                    last_error = e
                    if attempt == max_retries - 1:  # Last attempt
                        print(f"Failed after {max_retries} attempts. Last error: {str(last_error)}")
                        raise  # Re-raise the last error if all retries failed
                    if status_callback:
                        status_callback(f"API attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    if status_callback:
                        status_callback(f"Sending request to Claude API (attempt {attempt + 2}/3)...")
    
    def _get_media_type(self, image_path: str) -> str:
        ext = os.path.splitext(image_path)[1].lower()
        media_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        return media_types.get(ext, "image/jpeg")
