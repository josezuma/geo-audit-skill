#!/usr/bin/env python3
"""Validate the audit output JSON has expected fields."""
import json

d = json.load(open('audit_result.json'))
assert 'total_score' in d, 'Missing total_score'
assert 'checks' in d, 'Missing checks'
print(f'Score: {d["total_score"]}/100 — OK')
