"""Technology Stack Detection Agent"""
from typing import Dict, Any
import re
from bs4 import BeautifulSoup

class TechnologyReconnaissanceAgent:
    def __init__(self):
        self.confidence_thresholds = {
            'high': 85,
            'medium': 70,
            'low': 50
        }
