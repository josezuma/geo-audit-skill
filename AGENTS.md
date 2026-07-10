# geo-audit-skill

Claude/Agent skill that audits any URL for AI-search (GEO) readiness.

## For AI agents

- SKILL.md is the main entrypoint — agents load this when GEO auditing is needed
- `scripts/audit.py` runs standalone: `python scripts/audit.py <url>`
- Outputs scored JSON report + terminal report
- Sister skills: schema-for-ai, repo-visibility-skill
- Data dependency: ai-crawlers repo for robots.txt checks
