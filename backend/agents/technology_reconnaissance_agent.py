from typing import Dict, Any, List, Optional
import httpx
from bs4 import BeautifulSoup
import re
from .base_agent import BaseAgent
import asyncio
from datetime import datetime

class TechnologyReconnaissanceAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.tech_patterns = {
            'react': [r'react', r'_react', r'React\.', r'jsx'],
            'angular': [r'ng-', r'angular', r'Angular'],
            'vue': [r'vue', r'Vue\.', r'v-for', r'v-if'],
            'wordpress': [r'wp-content', r'wp-includes', r'wordpress'],
            'shopify': [r'shopify', r'myshopify\.com', r'cdn\.shopify'],
            'nextjs': [r'_next', r'next\.js', r'__NEXT_DATA__'],
            'gatsby': [r'gatsby', r'__GATSBY'],
            'django': [r'django', r'csrfmiddlewaretoken'],
            'rails': [r'rails', r'action_controller', r'active_record']
        }
    
    async def quick_tech_scan(self, url: str) -> Dict[str, Any]:
        """Quick technology scan"""
        content = await self._fetch_page_source(url)
        technologies = self._detect_technologies(content)
        
        return {
            "url": url,
            "technologies": technologies,
            "scan_type": "quick",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def deep_analysis(self, url: str) -> Dict[str, Any]:
        """Deep technology analysis including performance and security"""
        # Fetch various data points
        page_source = await self._fetch_page_source(url)
        headers = await self._fetch_headers(url)
        
        # Detect technologies
        technologies = self._detect_technologies(page_source)
        
        # Analyze with Claude
        system_prompt = """You are an expert technology analyst.
        Analyze the technical implementation of websites."""
        
        user_prompt = f"""Analyze this website's technology stack:
        
        URL: {url}
        Detected Technologies: {technologies}
        
        Headers (first 500 chars): {str(headers)[:500]}
        
        Provide analysis including:
        1. Technology stack assessment
        2. Performance implications
        3. Security considerations
        4. Scalability assessment
        5. Technical recommendations
        
        Respond in JSON format."""
        
        response = await self._call_claude(system_prompt, user_prompt)
        analysis = self._parse_json_response(response)
        
        return {
            "url": url,
            "detected_technologies": technologies,
            "headers": headers,
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _fetch_page_source(self, url: str) -> str:
        """Fetch page HTML source"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def _fetch_headers(self, url: str) -> Dict[str, str]:
        """Fetch HTTP headers"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.head(url)
                return dict(response.headers)
        except Exception as e:
            return {}
    
    def _detect_technologies(self, content: str) -> List[str]:
        """Detect technologies from page content"""
        detected = []
        content_lower = content.lower()
        
        for tech, patterns in self.tech_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    detected.append(tech)
                    break
        
        return list(set(detected))
