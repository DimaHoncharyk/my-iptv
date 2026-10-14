from urllib.request import Request, urlopen

SOURCES = [
    'https://iptv-org.github.io/iptv/countries/ru.m3u',
    'https://iptv-org.github.io/iptv/countries/ua.m3u',
]

entries = []
seen = set()
for source in SOURCES:
    request = Request(source, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(request, timeout=45) as response:
        lines = response.read().decode('utf-8-sig').splitlines()
    for i, line in enumerate(lines):
        if line.startswith('#EXTINF:'):
            chunk = [line]
            j = i + 1
            while j < len(lines) and not lines[j].startswith('#EXTINF:'):
                if lines[j].strip() and not lines[j].startswith('#EXTM3U'):
                    chunk.append(lines[j])
                j += 1
            urls = [x for x in chunk if not x.startswith('#')]
            if urls and urls[-1] not in seen:
                seen.add(urls[-1])
                entries.extend(chunk)

with open('playlist.m3u', 'w', encoding='utf-8') as file:
    file.write('#EXTM3U\n' + '\n'.join(entries) + '\n')
print(f'Updated playlist: {len(seen)} unique streams')
