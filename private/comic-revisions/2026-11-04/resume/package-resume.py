"""Package visually accepted imagegen outputs; no image content edits."""
import json, hashlib
from pathlib import Path
from PIL import Image
root=Path.home()/'dev/fullmetal_alchemist'
archive=root/'private/comic-revisions/2026-11-04/resume'
jobs=json.loads((archive/'results.json').read_text())
manifest=root/'site/data/comics.json'
chapters=json.loads(manifest.read_text())
protected={(3,'03-page-02-rev1.jpg'),(5,'05-page-04-rev1.jpg'),(8,'09-page-08-rev1.jpg'),(9,'08-page-07-rev1.jpg')}
original_map={}
for ch in chapters:
    for page in ch['pages']:
        original_map[(ch['number'],Path(page['original']).name)]=page
insertions=[]
for j in jobs:
    if j.get('status')!='verified': continue
    ch=next(c for c in chapters if c['number']==j['chapter'])
    old=j.get('old')
    if old:
        page=original_map[(j['chapter'],old)]
        assert (j['chapter'],Path(page['original']).name) not in protected
        stem=Path(old).stem+'-rev2'
        label=page['label']
    else:
        page={}
        stem=j['id']
        label=f"제{j['chapter']}화 · 보완 {j['insertOrder']}쪽"
        insertions.append((ch,j,page))
    src=archive/(j['id']+'.png')
    im=Image.open(src).convert('RGB')
    rel=Path('comics')/f"{j['chapter']:02d}"/(stem+'.jpg')
    dest=root/'site'/rel
    im.save(dest,quality=94,subsampling=0)
    digest=hashlib.sha256(dest.read_bytes()).hexdigest()[:12]
    paths={}
    for width in (720,1080):
        thumb=im.copy()
        thumb.thumbnail((width,100000))
        out=rel.with_name(f'{stem}-{digest}-{width}.webp')
        thumb.save(root/'site'/out,'WEBP',quality=85,method=6)
        paths[width]=out.as_posix()
    page.update(original=rel.as_posix(),src=paths[1080],small=paths[720],width=im.width,height=im.height,label=label,revisedAt='2026-11-05')
    j['publishedOriginal']=rel.as_posix()
for ch,j,page in sorted(insertions,key=lambda t:t[1]['insertOrder'],reverse=True):
    anchor=original_map[(j['chapter'],j['insertAfter'])]
    index=next(i for i,p in enumerate(ch['pages']) if p is anchor)
    ch['pages'].insert(index+1,page)
manifest.write_text(json.dumps(chapters,ensure_ascii=False,indent=2)+'\n')
(archive/'results.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2)+'\n')
print('Packaged',sum(j.get('status')=='verified' for j in jobs),'accepted pages')
