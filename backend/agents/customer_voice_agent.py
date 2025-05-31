from typing import Dict, Any, List
from .base_agent import BaseAgent
import httpx
from bs4 import BeautifulSoup
import re

class CustomerVoiceAgent(BaseAgent):
    def __init__(self):
        super().__init__()
    
    async def analyze_sentiment(self, target_url: str) -> Dict[str, Any]:
        """Analyze customer sentiment and voice from website content"""
        content = await self._fetch_testimonials_and_reviews(target_url)
        
        system_prompt = """You are an expert in customer sentiment analysis.
        Analyze website content to extract customer voice and sentiment insights."""
        
        user_prompt = f"""Analyze this website content for customer voice insights:
        
        URL: {target_url}
        Content: {content[:5000]}
        
        Provide analysis including:
        1. Customer sentiment overview
        2. Key customer pain points mentioned
        3. Value propositions that resonate
        4. Trust signals and social proof
        5. Customer language and terminology
        
        Respond in JSON format."""
        
        response = await self._call_claude(system_prompt, user_prompt)
        return self._parse_json_response(response)
    
    async def _fetch_testimonials_and_reviews(self, url: str) -> str:
        """Fetch content focusing on testimonials and reviews"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for testimonial sections
                testimonial_keywords = ['testimonial', 'review', 'customer', 'client', 'feedback']
                relevant_content = []
                
                for keyword in testimonial_keywords:
                    # Find divs or sections with these keywords in class or id
                    elements = soup.find_all(['div', 'section'], 
                                           class_=re.compile(keyword, re.I))
                    for elem in elements:
                        relevant_content.append(elem.get_text(strip=True))
                
                # Also get general text content
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                general_text = ' '.join(chunk for chunk in chunks if chunk)
                
                return ' '.join(relevant_content) + ' ' + general_text[:5000]
        except Exception as e:
            return f"Error: {str(e)}"
