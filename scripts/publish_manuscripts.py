"""Publish author-approved manuscript versions without rewriting the source text."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPECS=[
    {'id':'ms-prologue-v1','episode':'프롤로그','title':'연금술을 못 쓰는 연금술사','file':'000-prologue.md','order':0,'related':['m01']},
    {'id':'ms-001-v1','episode':'제1화','title':'동쪽으로 가는 길','file':'001-eastbound.md','order':1,'related':['m06','m04','m12']},
]
def main():
    path=ROOT/'site/data/project.json'
    project=json.loads(path.read_text('utf8'))
    manuscripts=[]
    for spec in SPECS:
        # Normalize platform newlines and optional file BOM only. Never edit prose.
        text=(ROOT/'manuscripts'/spec['file']).read_text('utf-8-sig').replace('\r\n','\n').rstrip('\n')
        manuscripts.append({**spec,'status':'DRAFT','version':1,'source':'manuscript-submission-v1','text':text,'characters':len(text),'sha256':hashlib.sha256(text.encode('utf8')).hexdigest()})
    project['manuscripts']=manuscripts
    project['version']='0.2.0'
    project['manuscriptSource']={'id':'manuscript-submission-v1','title':'사용자가 대화로 전달한 프롤로그와 제1화','note':'원문 v1. 교정·개작·원작 검증을 수행하지 않은 등록 원고. 제공한 회차의 초고이며 완성/검증 완료를 의미하지 않는다.'}
    project['narrativeDirection']={'source':'manuscript-submission-v1','notes':['에드가 명백한 주인공','알의 시점은 보여주지 않고 편지나 흔적으로만 존재','머스탱과 링은 필요할 때 짧게 시점 전환','스카의 형은 어떻게 연단술을 알았는가에서 출발해 이슈발라로 접근']}
    path.write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n','utf8')
    print('Published:',[(m['episode'],m['characters'],m['sha256'][:12]) for m in manuscripts])
if __name__=='__main__':main()
