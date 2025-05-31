from typing import Dict, Any, List
import httpx
from bs4 import BeautifulSoup
from .base_agent import BaseAgent
import asyncio
import re
import json
from datetime import datetime

class CompetitiveIntelligenceAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def analyze(self, target_url: str, competitors: List[str]) -> Dict[str, Any]:
        """Comprehensive competitive analysis"""
        # Fetch data for target and competitors
        all_sites = [target_url] + competitors
        site_data = await self._fetch_multiple_sites(all_sites)
        
        # Analyze competitive landscape
        analysis = await self._competitive_analysis(site_data, target_url)
        
        return analysis
    
    async def quick_positioning(self, target_url: str) -> Dict[str, Any]:
        """Quick competitive positioning analysis"""
        site_content = await self._fetch_site_content(target_url)
        
        system_prompt = """You are an expert competitive intelligence analyst.
        Analyze the website content and provide quick positioning insights."""
        
        user_prompt = f"""Analyze this website content and provide:
        1. Primary value proposition
        2. Target market
        3. Key differentiators
        4. Market positioning
        
        Website content (first 5000 chars):
        {site_content[:5000]}
        
        Respond in JSON format."""
        
        response = await self._call_claude(system_prompt, user_prompt)
        return self._parse_json_response(response)
    
    async def _fetch_site_content(self, url: str) -> str:
        """Fetch and parse website content"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.extract()
                
                # Get text content
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return text[:10000]  # Limit to first 10k chars
        except Exception as e:
            return f"Error fetching {url}: {str(e)}"
    
    async def _fetch_multiple_sites(self, urls: List[str]) -> Dict[str, str]:
        """Fetch multiple sites concurrently"""
        tasks = [self._fetch_site_content(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            url: result if isinstance(result, str) else str(result)
            for url, result in zip(urls, results)
        }
    
    async def _competitive_analysis(self, site_data: Dict[str, str], 
                                   target_url: str) -> Dict[str, Any]:
        """Perform comprehensive competitive analysis"""
        system_prompt = """You are an expert competitive intelligence analyst.
        Analyze multiple websites and provide strategic competitive insights."""
        
        # Prepare competitor data
        competitors_data = {
            url: content[:3000] for url, content in site_data.items()
            if url != target_url
        }
        
        user_prompt = f"""Perform a competitive analysis:
        
        TARGET WEBSITE: {target_url}
        Content: {site_data.get(target_url, 'Not available')[:3000]}
        
        COMPETITORS:
        {json.dumps(competitors_data, indent=2)}
        
        Provide analysis including:
        1. Competitive positioning matrix
        2. Feature comparison
        3. Pricing strategy analysis
        4. Strengths and weaknesses
        5. Market opportunities
        6. Strategic recommendations
        
        Respond in JSON format with detailed insights."""
        
        response = await self._call_claude(system_prompt, user_prompt)
        return self._parse_json_response(response)
