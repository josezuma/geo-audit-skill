#!/usr/bin/env python3
"""GEO Audit — audit a URL for AI-search readiness."""

import sys
import json
import urllib.request
import urllib.error
import re
from html.parser import HTMLParser

SCORE_PER_CHECK = 25

class AuditResult:
    def __init__(self, url):
        self.url = url
        self.llmstxt = {'score': 0, 'findings': []}
        self.robots = {'score': 0, 'findings': []}
        self.schema = {'score': 0, 'findings': []}
        self.citability = {'score': 0, 'findings': []}

    def total(self):
        return self.llmstxt['score'] + self.robots['score'] + self.schema['score'] + self.citability['score']

    def to_dict(self):
        return {
            'url': self.url,
            'checks': {
                'llms_txt': self.llmstxt,
                'robots_txt': self.robots,
                'json_ld_schema': self.schema,
                'citability': self.citability,
            },
            'total_score': self.total(),
            'max_score': 100,
        }


def fetch_url(url):
    """Fetch a URL and return (status, body, content_type)."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'GEO-Audit/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode('utf-8', errors='replace')
            return resp.status, body, resp.headers.get('Content-Type', '')
    except urllib.error.HTTPError as e:
        return e.code, '', ''
    except Exception as e:
        return 0, str(e), ''


def check_llmstxt(audit, domain):
    """Check for llms.txt and llms-full.txt."""
    for path in ['/llms.txt', '/llms-full.txt']:
        status, body, _ = fetch_url(f'https://{domain}{path}')
        if status == 200 and body.strip():
            audit.llmstxt['findings'].append(f'✅ {path} found ({len(body)} chars)')
        elif status == 200:
            audit.llmstxt['findings'].append(f'⚠️ {path} exists but is empty')
        else:
            audit.llmstxt['findings'].append(f'❌ {path} not found (HTTP {status})')
    if any('✅' in f for f in audit.llmstxt['findings']):
        audit.llmstxt['score'] = SCORE_PER_CHECK
    elif any('⚠️' in f for f in audit.llmstxt['findings']):
        audit.llmstxt['score'] = SCORE_PER_CHECK // 2


def check_robots(audit, domain):
    """Check robots.txt for AI crawler rules."""
    status, body, _ = fetch_url(f'https://{domain}/robots.txt')
    if status != 200:
        audit.robots['findings'].append(f'❌ robots.txt not found (HTTP {status})')
        return

    ai_crawlers = ['GPTBot', 'ClaudeBot', 'PerplexityBot', 'Google-Extended',
                   'CCBot', 'Bytespider', 'Amazonbot', 'OAI-SearchBot',
                   'cohere-ai', 'Anthropic-AI', 'Meta-ExternalAgent',
                   'Applebot', 'DuckDuckBot', 'Microsoft-AI',
                   'GrokSocial', 'SemrushBot']

    found = []
    for crawler in ai_crawlers:
        pattern = rf'User-agent:\s*{re.escape(crawler)}'
        if re.search(pattern, body, re.MULTILINE | re.IGNORECASE):
            found.append(crawler)

    if found:
        audit.robots['findings'].append(f'✅ {len(found)} AI crawlers explicitly configured: {", ".join(found[:5])}')
        # Check if any are disallowed
        disallowed = re.findall(r'User-agent:\s*(\S+).*?\nDisallow:\s*/', body, re.DOTALL)
        if disallowed:
            audit.robots['findings'].append(f'⚠️ Some crawlers blocked: {", ".join(d.strip() for d in disallowed[:3])}')
            audit.robots['score'] = SCORE_PER_CHECK // 2
        else:
            audit.robots['score'] = SCORE_PER_CHECK
    else:
        audit.robots['findings'].append('⚠️ No AI crawler rules found — models may crawl without explicit permission')
        audit.robots['score'] = SCORE_PER_CHECK // 2


class SchemaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.schemas = []
        self.in_ld_json = False
        self.buffer = ''

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'script' and attrs_dict.get('type') == 'application/ld+json':
            self.in_ld_json = True
            self.buffer = ''
        elif tag == 'script':
            self.in_ld_json = False

    def handle_data(self, data):
        if self.in_ld_json:
            self.buffer += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_ld_json and self.buffer.strip():
            try:
                parsed = json.loads(self.buffer)
                self.schemas.append(parsed)
            except json.JSONDecodeError:
                pass
            self.in_ld_json = False
            self.buffer = ''


def check_schema(audit, body):
    """Check for JSON-LD schema.org markup."""
    parser = SchemaParser()
    parser.feed(body)

    if not parser.schemas:
        audit.schema['findings'].append('❌ No JSON-LD structured data found')
        return

    types = set()
    for s in parser.schemas:
        if isinstance(s, dict):
            t = s.get('@type', '')
            if isinstance(t, list):
                types.update(t)
            else:
                types.add(t)
        elif isinstance(s, list):
            for item in s:
                t = item.get('@type', '') if isinstance(item, dict) else ''
                if isinstance(t, list):
                    types.update(t)
                else:
                    types.add(t)

    type_list = ', '.join(sorted(types)[:5])
    audit.schema['findings'].append(f'✅ {len(parser.schemas)} schema(s) found: {type_list}')
    audit.schema['score'] = SCORE_PER_CHECK


def check_citability(audit, body, domain):
    """Check for EEAT signals and citability patterns."""
    findings = []

    # Author byline
    author_patterns = [
        r'by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',  # "by John Smith"
        r'"author":\s*"([^"]+)"',               # JSON-LD author
        r'<meta\s+name="author"\s+content="([^"]+)"',
    ]
    for pat in author_patterns:
        match = re.search(pat, body)
        if match:
            findings.append(f'✅ Author found: {match.group(1)}')
            break
    else:
        findings.append('❌ No author byline found')

    # Publish date
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}',  # ISO date
        r'"datePublished":\s*"([^"]+)"',
        r'<time\s+datetime="([^"]+)"',
    ]
    for pat in date_patterns:
        if re.search(pat, body):
            findings.append('✅ Publish date found')
            break
    else:
        findings.append('⚠️ No publish date detected')

    # Statistics (numbers with % or numbers with context)
    stat_count = len(re.findall(r'\d+%|\d+x\s|over\s\d+|more than\s\d+', body, re.IGNORECASE))
    if stat_count >= 3:
        findings.append(f'✅ {stat_count} statistics/quotes found (strong citability)')
    elif stat_count >= 1:
        findings.append(f'⚠️ Only {stat_count} statistic(s) found (add more for better AI citation)')
    else:
        findings.append('❌ No verifiable statistics found')

    audit.citability['findings'] = findings
    audit.citability['score'] = sum([
        SCORE_PER_CHECK // 3 if '✅' in findings[0] else 0,
        SCORE_PER_CHECK // 3 if '✅' in findings[1] else 0,
        SCORE_PER_CHECK // 3 if '✅' in findings[2] else SCORE_PER_CHECK // 6 if '⚠️' in findings[2] else 0,
    ])


def score_label(score):
    if score >= 80:
        return '✅ Excellent GEO readiness'
    elif score >= 60:
        return '👍 Good — minor improvements needed'
    elif score >= 40:
        return '⚠️ Needs improvement'
    else:
        return '❌ Poor — significant work needed'


def main():
    if len(sys.argv) < 2:
        print('Usage: python audit.py <url>')
        sys.exit(1)

    url = sys.argv[1].strip().rstrip('/')
    if not url.startswith('http'):
        url = 'https://' + url

    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.netloc

    print(f'\n🔍 GEO Audit: {url}\n{"=" * 60}\n')

    # Fetch the page
    status, body, content_type = fetch_url(url)
    if status != 200:
        print(f'❌ Failed to fetch page: HTTP {status}')
        sys.exit(1)

    audit = AuditResult(url)

    check_llmstxt(audit, domain)
    check_robots(audit, domain)
    check_schema(audit, body)
    check_citability(audit, body, domain)

    total = audit.total()
    max_score = 100

    # Print report
    for check_name, check_data in [
        ('llms.txt', audit.llmstxt),
        ('robots.txt (AI crawlers)', audit.robots),
        ('JSON-LD Schema', audit.schema),
        ('Citability (EEAT)', audit.citability),
    ]:
        score = check_data['score']
        bar = '█' * (score // 5) + '░' * ((SCORE_PER_CHECK - score) // 5)
        print(f'\n📋 {check_name:30s} {score:3d}/{SCORE_PER_CHECK}')
        print(f'   {bar}')
        for f in check_data['findings']:
            print(f'   {f}')

    print(f'\n{"=" * 60}')
    print(f'📊 TOTAL SCORE: {total}/{max_score} — {score_label(total)}')
    print(f'{"=" * 60}\n')

    # Output JSON to file
    with open('audit_result.json', 'w') as f:
        json.dump(audit.to_dict(), f, indent=2)
    print('Full report saved to audit_result.json')


if __name__ == '__main__':
    main()
