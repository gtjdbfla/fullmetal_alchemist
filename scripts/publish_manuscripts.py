"""Publish author-approved manuscript versions without rewriting the source text."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPECS=[
    {'id':'ms-prologue-v1','episode':'프롤로그','title':'연금술을 못 쓰는 연금술사','file':'000-prologue.md','order':0,'version':1,'related':['m01']},
    {'id':'ms-001-v1','episode':'제1화','title':'동쪽으로 가는 길','file':'001-eastbound.md','order':1,'version':3,'related':['m06','m04','m12']},
    {'id':'ms-002-v1','episode':'제2화','title':'신의 이름','file':'002-name-of-god.md','order':2,'version':2,'related':['m06','m09','m14']},
]
def main():
    path=ROOT/'site/data/project.json'
    project=json.loads(path.read_text('utf8'))
    manuscripts=[]
    for spec in SPECS:
        # Normalize platform newlines and optional file BOM only. Never edit prose.
        text=(ROOT/'manuscripts'/spec['file']).read_text('utf-8-sig').replace('\r\n','\n').rstrip('\n')
        manuscripts.append({**spec,'status':'DRAFT','source':'manuscript-submission-v2' if spec['order']==2 else 'manuscript-submission-v1','text':text,'characters':len(text),'sha256':hashlib.sha256(text.encode('utf8')).hexdigest()})
    project['manuscripts']=manuscripts
    project['version']='0.3.0'
    project['proofreading']=json.loads((ROOT/'docs/PROOFREADING.json').read_text('utf8'))
    for m in manuscripts:
        m['revisionNote']={0:'제출 원고 · 문장 변경 없음',1:'지명 오타 교정 후, 서부 국경지역 대표로 수정 · 원본 v1·v2 보존',2:'사용자 승인: 연구 경로의 확정 표현을 가설로 교정 · 원본 v1 보존'}[m['order']]
    project['analysis']=json.loads((ROOT/'docs/STORY_REVIEW.json').read_text('utf8'))
    project['manuscriptSource']={'id':'manuscript-submission-v1','title':'사용자가 대화로 전달하고 교정을 승인한 프롤로그·제1화·제2화','note':'프롤로그 v1·제1화 교정본 v3·제2화 교정본 v2. 승인된 수정과 이전 버전을 보존한다. 설정 확정과 실제 떡밥 회수는 별도다.'}
    project['narrativeDirection']={'source':'manuscript-submission-v1','notes':['에드가 명백한 주인공','알의 시점은 보여주지 않고 편지나 흔적으로만 존재','머스탱과 링은 필요할 때 짧게 시점 전환','스카의 형은 어떻게 연단술을 알았는가에서 출발해 이슈발라로 접근']}
    path.write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n','utf8')
    print('Published:',[(m['episode'],m['characters'],m['sha256'][:12]) for m in manuscripts])
if __name__=='__main__':main()
