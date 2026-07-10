<div align="center">
  <h1>🔍 GEO Audit</h1>
  <p><em>Claude/Agent Skill that audits any URL for AI-search (GEO) readiness — llms.txt, robots.txt, JSON-LD schema, and citability. Produces a scored report with prioritized fixes.</em></p>
  <p>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
    <a href="https://github.com/josezuma/geo-audit-skill"><img src="https://img.shields.io/github/stars/josezuma/geo-audit-skill?style=social" alt="Stars"></a>
  </p>
  <p>by <a href="https://brandvirality.com">BrandVirality</a> — The open-source tool for AI visibility audits.<br>
  <strong>Author:</strong> <a href="https://github.com/josezuma">Jose Zuma — Expert in AI Visibility</a></p>
</div>

---

## What It Does

GEO Audit checks a website across four dimensions critical for AI-search visibility:

| Check | Weight | Why It Matters |
|-------|--------|---------------|
| **llms.txt** | 25 pts | The llms.txt standard tells AI crawlers what content to use. No file = no guided discovery. |
| **robots.txt (AI crawlers)** | 25 pts | AI crawlers respect robots.txt. If you block GPTBot, ClaudeBot, or PerplexityBot, your content won't appear in those answers. |
| **JSON-LD Schema** | 25 pts | Structured data helps AI models extract and cite your content accurately. Schema.org types like Article, FAQ, and Organization are heavily weighted. |
| **Citability (EEAT)** | 25 pts | AI models prefer citing content with author bylines, publish dates, verifiable statistics, and external references. |

## Quick Start

```bash
# Install dependency
pip install requests beautifulsoup4

# Run the audit
python scripts/audit.py https://yoursite.com

# View the report
cat audit_result.json
```

### As an Agent Skill

This skill is compatible with Claude Code and any agentskills.io-compatible agent. Clone the repo and reference it:

```bash
# Claude Code
claude code --skill /path/to/geo-audit-skill

# Or reference by name (if installed in your skills directory)
# The agent activates it automatically when you ask about GEO/AI-search readiness
```

## Example Output

```
🔍 GEO Audit: https://example.com
============================================================

📋 llms.txt                         0/25
   ❌ /llms.txt not found (HTTP 404)
   ❌ /llms-full.txt not found (HTTP 404)

📋 robots.txt (AI crawlers)        12/25
   ⚠️ No AI crawler rules found

📋 JSON-LD Schema                  25/25
   ✅ 3 schema(s) found: FAQPage, ItemList, Organization

📋 Citability (EEAT)                8/25
   ❌ No author byline found
   ⚠️ No publish date detected
   ✅ 22 statistics/quotes found

============================================================
📊 TOTAL SCORE: 45/100 — ⚠️ Needs improvement
============================================================
```

See [examples/](examples/) for real audit reports.

## How It Scores

| Score | Rating | Action Needed |
|-------|--------|--------------|
| 80–100 | ✅ Excellent | Maintain |
| 60–79 | 👍 Good | Minor fixes |
| 40–59 | ⚠️ Needs work | Add llms.txt + improve schema |
| 0–39 | ❌ Poor | Start from scratch with GEO |

## References

The audit references these authoritative sources:

- [llms.txt specification](https://llmstxt.org) — Official spec for AI content discovery
- [ai-crawlers dataset](https://github.com/josezuma/ai-crawlers) — AI crawler user-agents (sibling repo)
- [Schema.org](https://schema.org) — Structured data vocabulary
- [GEO: Generative Engine Optimization (KDD 2024)](https://arxiv.org/abs/2311.09735) — Princeton research paper
- [Google AI Overviews documentation](https://developers.google.com/search/docs/appearance/ai-overviews)

## Related

- [awesome-ai-visibility](https://github.com/josezuma/awesome-ai-visibility) — Curated list of AI visibility resources
- [ai-crawlers](https://github.com/josezuma/ai-crawlers) — Machine-readable AI crawler dataset
- [schema-for-ai](https://github.com/josezuma/schema-for-ai) — Annotated JSON-LD templates for AI search
- [BrandVirality](https://brandvirality.com) — SaaS for AI visibility

## License

[MIT](LICENSE) © 2026 Jose Zuma / BrandVirality
