from typing import Dict, Any, List, Optional
from anthropic import Anthropic
import os
from datetime import datetime
import json

class BaseAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-opus-20240229"
        self.agent_name = self.__class__.__name__
        self.created_at = datetime.utcnow()
    
    async def analyze(self, *args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("Each agent must implement analyze method")
    
    async def _call_claude(self, system_prompt: str, user_prompt: str, 
                          max_tokens: int = 4000) -> str:
        """Call Claude API with error handling"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            raise
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Safely parse JSON from Claude response"""
        try:
            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            return {"raw_response": response}
        except json.JSONDecodeError:
            return {"raw_response": response}
