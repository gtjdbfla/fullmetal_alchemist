import json, hashlib
from pathlib import Path
from PIL import Image
root=Path.home()/'dev/fullmetal_alchemist'
a=json.loads((root/'private/comic-revisions/2026-11-04/resume/results.json').read_text())
manifest=json.loads((root/'site/data/comics.json').read_text())
count=0
for j in a:
 if j['status']!='verified': continue
 p=next(p for c in manifest for p in c['pages'] if p['original']==j['publishedOriginal'])
 original=root/'site'/p['original']
 digest=hashlib.sha256(original.read_bytes()).hexdigest()[:12]
 with Image.open(original) as source:
  source=source.convert('RGB')
  for width,key in [(720,'small'),(1080,'src')]:
   path=root/'site'/p[key]
   assert digest in path.name
   height=round(source.height*width/source.width)
   source.resize((width,height),Image.Resampling.LANCZOS).save(path,'WEBP',quality=85,method=6)
   with Image.open(path) as check: assert check.width==width
 count+=1
for c in manifest:
 for p in c['pages']:
  for key in ['original','small','src']: assert (root/'site'/p[key]).is_file(),p[key]
print('Validated',count,'revisions and all manifest files')
