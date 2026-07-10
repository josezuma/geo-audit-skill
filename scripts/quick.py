#!/usr/bin/env python3
"""Quick GEO snapshot — 60-second check of a URL's AI-search readiness."""
import json, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.audit import AuditResult, fetch_url, check_llmstxt, check_robots

def quick_audit(url):
    from urllib.parse import urlparse
    domain = urlparse(url).netloc
    
    print(f'\n⚡ Quick GEO Snapshot: {url}')
    print('=' * 50)
    
    status, body, _ = fetch_url(url)
    if status != 200:
        print(f'❌ Site unreachable (HTTP {status})')
        return
    
    audit = AuditResult(url)
    check_llmstxt(audit, domain)
    check_robots(audit, domain)
    
    print(f'  llms.txt: {"✅" if audit.llmstxt["score"] > 0 else "❌"}')
    print(f'  robots.txt AI rules: {"✅" if audit.robots["score"] > 0 else "⚠️"}')
    print(f'  Site reachable: ✅ (HTTP {status})')
    print(f'  Content length: {len(body):,} chars')
    print(f'\n  Quick score: {audit.total()}/50 (llms.txt + robots.txt only)')

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://example.com'
    quick_audit(url)
