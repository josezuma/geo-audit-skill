---
name: geo-audit
description: Audits a URL for AI-search (GEO) readiness. Checks llms.txt presence, robots.txt AI-crawler rules, JSON-LD schema.org markup, and citability patterns. Outputs a scored report with prioritized fixes. Use when analyzing a website for Generative Engine Optimization (GEO), AI search visibility, or preparing content for LLM citation.
license: MIT
metadata:
  author: brandvirality
  version: "1.0.0"
compatibility: Requires Python 3.10+, `pip install requests beautifulsoup4` for standalone mode
---

# GEO Audit Skill

Audits any URL for AI-search (Generative Engine Optimization) readiness. Runs four checks and produces a scored report with actionable fixes.

## Quick Start

```bash
# Standalone usage (no agent needed)
pip install requests beautifulsoup4
python scripts/audit.py https://example.com
```

As an agent skill, this SKILL.md is loaded automatically by agent-compatible systems.

## Checks Performed

### 1. llms.txt Check (25 points)
- Does the site serve an `/llms.txt` file?
- Does `/llms-full.txt` exist?
- Are the entries valid per the llmstxt.org spec?

### 2. robots.txt AI Crawler Check (25 points)
- Does `/robots.txt` explicitly allow or block AI crawlers?
- Are GPTBot, ClaudeBot, PerplexityBot, Google-Extended configured?
- If blocked, the site won't be cited by those AI models.

### 3. JSON-LD Schema Check (25 points)
- Does the page have JSON-LD structured data?
- Which schema.org types are used (Organization, Article, FAQ, Product, etc.)?
- Are the schemas valid JSON-LD?
- AI models heavily weight structured data for extraction and citation.

### 4. Citability Check (25 points)
- Does the page contain verifiable statistics, quotes, or definitions?
- Are there author bylines with real names (EEAT signal)?
- Is there a publish date?
- Does the page have external reference links?

## Scoring

Scores range 0-100 across the four dimensions above. Results include specific findings and prioritized fixes.

## Example Output

```
GEO Audit Report for https://example.com
==========================================
llms.txt:        ❌ Not found (-25 pts)
robots.txt:      ⚠️ No AI crawler rules (-15 pts)
JSON-LD Schema:  ✅ Organization + Article present (+20 pts)
Citability:      ✅ Author bio, publish date, 3 statistics (+20 pts)
----------------------------------------
TOTAL SCORE:     55/100 — Needs improvement
```

## References

- [llms.txt specification](https://llmstxt.org)
- [AI crawler dataset (ai-crawlers)](https://github.com/josezuma/ai-crawlers)
- [Schema.org](https://schema.org)
- [GEO research paper (KDD 2024)](https://arxiv.org/abs/2311.09735)

## Related

- [[ai-crawlers]] — AI crawler user-agent dataset
- [[schema-for-ai]] — Annotated JSON-LD templates
- [[repo-visibility-skill]] — Same concept but for GitHub repos
