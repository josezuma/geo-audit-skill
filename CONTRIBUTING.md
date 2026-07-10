# Contributing to geo-audit-skill

Thanks for contributing!

## How to Contribute

1. **Report issues** — Open a GitHub issue for bugs or feature requests.
2. **Submit PRs** — Fork, make your changes, and submit a pull request.
3. **Add audit checks** — New checks (e.g., OpenGraph, hreflang, Core Web Vitals) are welcome.

## Development

```bash
pip install requests beautifulsoup4
python scripts/audit.py https://example.com
```

## Standards

- Follow the existing code style
- Include tests for new audit checks
- Update the SKILL.md docs if adding new features
- Run against at least one real URL before committing
