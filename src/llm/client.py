"""
OpenAI Client for LLM interactions
Handles API calls, rate limiting, and error handling
"""

import os
from typing import Optional, Dict, List, Any
from openai import OpenAI
from dotenv import load_dotenv
import time
import json


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
        
        # Initialize client
        self.client = OpenAI(api_key=self.api_key)
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
        try:
            # Make API call
            params = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if response_format:
                params["response_format"] = response_format
            
            response = self.client.chat.completions.create(**params)
            
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
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
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
