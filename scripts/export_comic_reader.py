"""Build comic readers with inline styles and first images for high-latency connections."""
from pathlib import Path
import base64
import html
import json
import re
from navigation import render_navigation

ROOT = Path(__file__).resolve().parents[1]

def export():
    site = ROOT / 'site'
    chapters = json.loads((site / 'data/comics.json').read_text(encoding='utf-8'))
    template = (site / 'index.html').read_text(encoding='utf-8')
    css = (site / 'style.css').read_text(encoding='utf-8')
    template = template.replace('<link rel="stylesheet" href="./style.css">', '<style>' + css + '.comic-toc{margin-bottom:24px}.comic-toc summary{cursor:pointer;padding:16px}.comic-reader{max-width:900px}.comic-reader img{height:auto}a.comic-move{padding:12px;border:1px solid #65776b;border-radius:6px;color:inherit;text-decoration:none}</style>')
    template = template.replace('href="./mark.svg"', 'href="/east/mark.svg"').replace('src="./mark.svg"', 'src="/east/mark.svg"')
    template = re.sub(r'(<nav id="navigation"[^>]*>).*?(</nav>)', lambda match: match[1] + render_navigation('comic') + match[2], template, flags=re.S)
    template = template.replace('<b id="breadcrumb">글 읽기</b>', '<b id="breadcrumb">만화 읽기</b>')
    template = template.replace('<script type="module" src="./app.js"></script>', '')
    dest = site / 'comics/read'
    dest.mkdir(parents=True, exist_ok=True)
    esc = lambda value: html.escape(str(value), quote=True)
    # Supplemental chapter IDs leave the existing numbered reader URLs in place.
    legacy_ids = iter(range(len(chapters)))
    reader_ids = [
        chapter['readerId'] if 'readerId' in chapter else str(next(legacy_ids))
        for chapter in chapters
    ]
    for index, chapter in enumerate(chapters):
        label = esc(chapter['episode'] + ' · ' + chapter['title'])
        toc = '<details class="comic-toc" id="toc"><summary>회차 목차 · ' + label + '</summary><nav class="chapter-index" aria-label="만화 목차">'
        for i, item in enumerate(chapters):
            toc += f'<a class="comic-move" href="/east/comics/read/{reader_ids[i]}.html"' + (' aria-current="page"' if i == index else '') + '>' + esc(item['episode'] + ' · ' + item['title']) + '</a>'
        toc += '</nav></details>'
        body = toc + '<article class="comic-reader"><header><span>만화 읽기 · ' + esc(chapter['episode']) + '</span><h1>' + esc(chapter['title']) + '</h1><p>비공식 팬 만화 · 왼쪽에서 오른쪽으로 읽어 주세요.</p></header>'
        for i, page in enumerate(chapter['pages']):
            if i < 2:
                data = base64.b64encode((site / page['small']).read_bytes()).decode('ascii')
                image = f'<img src="data:image/webp;base64,{data}"'
            else:
                image = '<img src="/east/' + esc(page['small']) + '" srcset="/east/' + esc(page['small']) + ' 720w, /east/' + esc(page['src']) + ' 1080w" sizes="(max-width:760px) 100vw, 900px" loading="lazy"'
            body += '<figure><a href="/east/' + esc(page['original']) + '" target="_blank" rel="noopener">' + image + f' width="{page["width"]}" height="{page["height"]}" alt="' + esc(page['label']) + '"></a><figcaption>' + esc(page['label']) + '</figcaption></figure>'
        body += '<nav class="chapter-controls" aria-label="만화 이동">'
        if index > 0: body += f'<a class="comic-move" href="/east/comics/read/{reader_ids[index - 1]}.html">← 이전화</a>'
        body += '<a class="comic-move" href="#toc">맨 위로 · 목차</a>'
        if index + 1 < len(chapters): body += f'<a class="comic-move" href="/east/comics/read/{reader_ids[index + 1]}.html">다음화 →</a>'
        body += '</nav></article>'
        output = template.replace('<main id="main"><div class="loading">기록을 펼치는 중</div></main>', '<main id="main">' + body + '</main>')
        (dest / f'{reader_ids[index]}.html').write_text(output, encoding='utf-8')
    return len(chapters)
