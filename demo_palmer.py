"""Demo script showing Palmer Intelligence capabilities"""
import asyncio
import httpx
import json
from datetime import datetime

async def demo_palmer_intelligence():
    """Demonstrate the power of Palmer Intelligence"""
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient(timeout=60) as client:
        print("🚀 Palmer Intelligence Demo")
        print("=" * 50)
        
        # 1. Quick Competitive Scan
        print("\n1. Running Quick Competitive Scan on Stripe...")
        response = await client.post(
            f"{base_url}/api/v1/quick-competitive-scan",
            params={"target_url": "stripe.com"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis completed in {result['data']['metadata']['execution_time']}")
            print(f"📊 Competitors found: {result['data']['metadata']['competitors_analyzed']}")
            print("\n🎯 Executive Summary:")
            for finding in result['data']['executive_summary']['key_findings'][:3]:
                print(f"  • {finding}")
        
        # 2. Generate Industry Report
        print("\n\n2. Generating Payment Processing Industry Report...")
        response = await client.post(
            f"{base_url}/api/v1/generate-industry-report",
            json={
                "industry": "Payment Processing",
                "company_urls": [
                    "stripe.com",
                    "paypal.com",
                    "square.com",
                    "adyen.com"
                ],
                "report_type": "comprehensive"
            }
        )
        
        if response.status_code == 200:
            report = response.json()
            print("✅ Industry Report Generated!")
            print("\n📰 Viral Headlines for LinkedIn:")
            for headline in report['viral_headlines']:
                print(f"  • {headline}")
        
        print("\n" + "=" * 50)
        print("🎉 Demo Complete! Visit http://localhost:8000/docs for full API documentation")

if __name__ == "__main__":
    asyncio.run(demo_palmer_intelligence())
