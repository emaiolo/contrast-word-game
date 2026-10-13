#!/usr/bin/env python3
"""Download a small date window of official Wordle solutions for static hosting."""
import json
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

base = datetime.now(ZoneInfo('America/New_York')).date()
result = {}
for offset in range(-2, 4):
    day = (base + timedelta(days=offset)).isoformat()
    url = f'https://www.nytimes.com/svc/wordle/v2/{day}.json'
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; AccessibleWordGame/1.0)', 'Accept': 'application/json'})
        with urllib.request.urlopen(request, timeout=18) as response:
            obj = json.load(response)
        answer = str(obj.get('solution', '')).upper()
        if len(answer) != 5 or not answer.isalpha() or not answer.isascii():
            raise ValueError('Invalid solution')
        result[day] = {'answer': answer, 'number': obj.get('days_since_launch')}
        print(day, 'OK')
    except Exception as exc:
        print(day, 'NOT AVAILABLE:', exc)
if not result:
    raise SystemExit('No daily puzzle data could be downloaded; refusing to publish an empty file')
Path('puzzles.json').write_text(json.dumps({'updated_at': datetime.now(ZoneInfo('UTC')).isoformat(), 'puzzles': result}, indent=2) + '\n', encoding='utf-8')
