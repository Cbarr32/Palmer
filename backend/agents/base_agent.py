"""Base Agent with Anthropic Integration"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import os
import logging
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all Palmer Intelligence agents"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    @abstractmethod
    async def analyze(self, data: Any) -> Dict[str, Any]:
        """Analyze data - must be implemented by subclasses"""
        pass
        
    async def think(self, prompt: str, temperature: float = 0.7) -> str:
        """Use Claude for intelligent analysis"""
        try:
            response = await self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                temperature=temperature,
                system=f"You are {self.name}, {self.role}",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error in {self.name}: {str(e)}")
            raise
