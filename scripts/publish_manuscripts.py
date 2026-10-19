"""Publish author-approved manuscript versions without rewriting the source text."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPECS=[
    {'id':'ms-prologue-v1','episode':'프롤로그','title':'연금술을 못 쓰는 연금술사','file':'000-prologue.md','order':0,'version':2,'related':['m01']},
    {'id':'ms-001-v1','episode':'제1화','title':'동쪽으로 가는 길','file':'001-eastbound.md','order':1,'version':5,'related':['m06','m04','m12']},
    {'id':'ms-002-v1','episode':'제2화','title':'신의 이름','file':'002-name-of-god.md','order':2,'version':4,'related':['m06','m09','m14','m15','m16']},
]
def main():
    path=ROOT/'site/data/project.json'
    project=json.loads(path.read_text('utf8'))
    manuscripts=[]
    for spec in SPECS:
        # Normalize platform newlines and optional file BOM only. Never edit prose.
        text=(ROOT/'manuscripts'/spec['file']).read_text('utf-8-sig').replace('\r\n','\n').rstrip('\n')
        manuscripts.append({**spec,'status':'DRAFT','source':'manuscript-continuous-draft','text':text,'characters':len(text),'sha256':hashlib.sha256(text.encode('utf8')).hexdigest()})
    project['manuscripts']=manuscripts
    compiled='강철의 연금술사 - 동쪽으로\n\n'+'\n\n⸻\n\n'.join(m['text'] for m in manuscripts)+'\n'
    (ROOT/'manuscripts/continuous-prologue-02.md').write_text(compiled,'utf8')
    project['version']='0.3.0'
    project['proofreading']=json.loads((ROOT/'docs/PROOFREADING.json').read_text('utf8'))
    for m in manuscripts:
        m['revisionNote']={0:'새 연속 수정본 · 본문 그대로 보존 · 이전 v1 보존',1:'새 연속 수정본 · 리젬블 → 리셈블 1곳 통일 · 수신 원문·이전 버전 보존',2:'새 연속 수정본 · 연구 노트 띄어쓰기 1곳 통일 · 수신 원문·이전 버전 보존'}[m['order']]
    project['analysis']=json.loads((ROOT/'docs/STORY_REVIEW.json').read_text('utf8'))
    project['manuscriptSource']={'id':'manuscript-continuous-draft','title':'사용자가 새로 제출한 프롤로그~2화 연속 수정본','note':'프롤로그 v2·제1화 v5·제2화 v4. 수신 원문과 이전 버전 보존. 지명·띄어쓰기 2곳 외 새 제출 본문은 그대로이며, 내용 제안은 별도 검토로 남긴다.'}
    project['narrativeDirection']={'source':'manuscript-submission-v1','notes':['에드가 명백한 주인공','알의 시점은 보여주지 않고 편지나 흔적으로만 존재','머스탱과 링은 필요할 때 짧게 시점 전환','스카의 형은 어떻게 연단술을 알았는가에서 출발해 이슈발라로 접근']}
    path.write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n','utf8')
    print('Published:',[(m['episode'],m['characters'],m['sha256'][:12]) for m in manuscripts])
if __name__=='__main__':main()
