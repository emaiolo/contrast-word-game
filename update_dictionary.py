"""Build a permissive offline five-letter dictionary for the browser game."""
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
request = Request(SOURCE, headers={'User-Agent': 'contrast-word-game/1.1'})
with urlopen(request, timeout=45) as response:
    source_text = response.read().decode('utf-8')
words = sorted({word.strip().upper() for word in source_text.splitlines()
                if len(word.strip()) == 5 and word.strip().isascii() and word.strip().isalpha()})
if len(words) < 3000:
    raise RuntimeError(f'Dictionary download appears incomplete: {len(words)} words')
Path(__file__).with_name('words5.txt').write_text('\n'.join(words) + '\n', encoding='utf-8')
print(f'Wrote {len(words):,} five-letter words')
