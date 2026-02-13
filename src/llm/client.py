"""
OpenAI Client for LLM interactions
Handles API calls, rate limiting, and error handling
"""

import os
import ssl
from typing import Optional, Dict, List, Any
from openai import OpenAI
from dotenv import load_dotenv
import time
import json
import httpx


class LLMClient:
    """Wrapper for OpenAI API with rate limiting and error handling"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key (loads from env if None)
            model: Model to use (default: gpt-4o)
        """
        # Load environment variables
        load_dotenv()
        
        # Get API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY in .env file or pass as parameter"
            )
        
        # Create HTTP client with SSL verification disabled if requested
        http_client = None
        disable_ssl = os.getenv("DISABLE_SSL_VERIFY", "").lower() in ("true", "1", "yes")
        
        # Set timeout - default 10 minutes for large responses (600 seconds)
        timeout = httpx.Timeout(
            timeout=600.0,  # Total timeout
            connect=10.0,   # Connection timeout
            read=300.0,     # Read timeout (5 minutes)
            write=30.0      # Write timeout
        )
        
        if disable_ssl:
            http_client = httpx.Client(
                verify=False, 
                follow_redirects=True,
                timeout=timeout
            )
        else:
            http_client = httpx.Client(timeout=timeout)
        
        # Initialize client
        self.client = OpenAI(api_key=self.api_key, http_client=http_client)
        self.model = model
        
        # Track usage
        self.total_tokens = 0
        self.total_cost = 0.0
        self.call_count = 0
        
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Call OpenAI chat completion API
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            response_format: Optional response format (e.g., {"type": "json_object"})
            
        Returns:
            Dict with 'content', 'tokens', 'cost'
        """
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                # Make API call
                params = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                }
                
                # GPT-5 uses max_completion_tokens instead of max_tokens
                if self.model.startswith("gpt-5") or self.model.startswith("o1"):
                    params["max_completion_tokens"] = max_tokens
                else:
                    params["max_tokens"] = max_tokens
                
                if response_format:
                    params["response_format"] = response_format
                
                response = self.client.chat.completions.create(**params)
                
                # Debug: Check if response is valid
                if isinstance(response, str):
                    raise ValueError(f"Unexpected string response from API. This may indicate a proxy/firewall issue. Response: {response[:500]}")
                
                # Extract response
                content = response.choices[0].message.content
                
                # Calculate usage
                tokens_used = response.usage.total_tokens
                cost = self._calculate_cost(tokens_used)
                
                # Update tracking
                self.total_tokens += tokens_used
                self.total_cost += cost
                self.call_count += 1
                
                return {
                    "content": content,
                    "tokens": tokens_used,
                    "cost": cost,
                    "finish_reason": response.choices[0].finish_reason
                }
                
            except KeyboardInterrupt:
                # Don't retry on actual user interrupts
                raise
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"API call failed (attempt {attempt + 1}/{max_retries}): {e}")
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print(f"Error calling OpenAI API after {max_retries} attempts: {e}")
                    raise
    
    def vision_analysis(
        self,
        image_data: str,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Dict[str, Any]:
        """
        Analyze image with GPT-4o Vision
        
        Args:
            image_data: Base64 encoded image or image URL
            prompt: Analysis prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Dict with 'content', 'tokens', 'cost'
        """
        # Determine if base64 or URL
        if image_data.startswith("http"):
            image_url = image_data
        else:
            # Assume base64
            image_url = f"data:image/jpeg;base64,{image_data}"
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
        
        return self.chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def _calculate_cost(self, tokens: int) -> float:
        """
        Calculate cost based on token usage
        
        GPT-4o pricing (as of 2024):
        - Input: $5 / 1M tokens
        - Output: $15 / 1M tokens
        - Simplified average: $10 / 1M tokens
        
        Args:
            tokens: Total tokens used
            
        Returns:
            Estimated cost in USD
        """
        cost_per_million = 10.0  # Average cost
        return (tokens / 1_000_000) * cost_per_million
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics
        
        Returns:
            Dict with tokens, cost, call_count
        """
        return {
            "total_tokens": self.total_tokens,
            "total_cost": round(self.total_cost, 4),
            "call_count": self.call_count,
            "avg_tokens_per_call": round(self.total_tokens / max(self.call_count, 1), 2)
        }
    
    def reset_stats(self):
        """Reset usage statistics"""
        self.total_tokens = 0
        self.total_cost = 0.0
        self.call_count = 0


# Helper function for quick usage
def create_llm_client(model: str = "gpt-4o") -> LLMClient:
    """
    Create and return an LLM client instance
    
    Args:
        model: Model to use
        
    Returns:
        LLMClient instance
    """
    return LLMClient(model=model)
