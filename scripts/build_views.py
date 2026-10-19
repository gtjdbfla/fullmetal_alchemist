"""Build distinct reader/author snapshots. Private truth never ships to public static assets."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
from publish_manuscripts import main as publish_manuscripts
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text('utf8'))
def dump(p,value):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n','utf8')
def projections(shared,legacy,master):
    author=deepcopy(legacy)
    for key in ['manuscripts','proofreading','analysis','manuscriptSource','narrativeDirection']:author[key]=deepcopy(shared[key])
    author.update(deepcopy(master))
    author.update(version='0.4.0',audience='author',revealedThrough=2,masterVersion='1.0')
    author['acts']=[{'id':x['id'],'title':x['label'],'name':x['title'],'place':'구체 화수 미정' if x['status']=='PLANNED' else '등록 원고','text':x['summary']} for x in master['masterPlan']['roadmap']]
    author['chapterRoadmap']=deepcopy(master['masterPlan']['roadmap'])
    author['timelineLanes']=[['EDWARD','이슈발 조사 → 사막·옛길 → 최종 사막 재회 → 함께 싱'],['ALPHONSE','싱에서 출발 → 동쪽에서 서쪽으로 같은 길 조사 → 최종 사막 재회'],['LING','황제의 통치 → 교역로·부족 갈등 → 지역의 결정 존중'],['MUSTANG / MILES','재건의 책임 → 조사·결정권 갈등 → 이슈발의 결정 지원']]
    author['characters'][0]['change']='진리를 본 경험으로 오답 가설을 확신하다가, 모든 것을 알 수 없음을 받아들인다.'
    author['characters'][1]['change']='POV를 숨긴다. 편지·기록·타인의 언급만 보이고 최종편 사막에서 형과 재회한다. 중반 싱 합류는 폐기된 초기 구상이다.'
    author['principles'][3]['text']='이슈발라 = 진리 또는 용맥을 최종 해답으로 확정하지 않는다. 에드가 이슈발라 = 진리라는 오답을 확신하는 전개는 허용하며 실제 설정과 분리한다.'
    author['analysis']['findings'][1]['reason']+=' 새 마스터 플랜에서 연구의 출발점은 이슈발로 확정됐지만, 작가의 정답이 2화 에드의 근거 부족을 자동 해결하지는 않는다.'
    public=deepcopy(shared)
    public.update(version='0.4.0',audience='reader',revealedThrough=2,masterVersion='1.0')
    public['masterPlan']=None
    public['masterAlignment']=None
    public['disclosureBoard']=[{'id':x['id'],'title':x['title'],'asOfEpisode':x['asOfEpisode'],'readerKnowledge':deepcopy(x['readerKnowledge']),'edHypothesis':deepcopy(x['edHypothesis']),'actualSetting':None,'revealPlan':None,'restricted':True} for x in master['disclosureBoard']]
    public['chapterRoadmap']=[deepcopy(x) for x in master['masterPlan']['roadmap'] if x.get('publishedThrough',99)<=2]
    public['acts']=[{'id':'prologue','title':'프롤로그','name':'서쪽 여행','place':'서쪽 국가','text':'광산 사고에서 연금술 대신 지식으로 문제를 푸는 에드.'},{'id':'ep01','title':'제1화','name':'귀환과 편지','place':'리셈블 → 센트럴 → 동부행','text':'알의 질문을 받은 에드는 이슈발을 먼저 조사하기로 한다. 링에게 옛길 개방 요청이 들어온다.'},{'id':'ep02','title':'제2화','name':'신의 이름','place':'이슈발','text':'마일즈·스카와 재건 현장을 보고 기도소에서 형의 노트를 발견한다. 연구의 시작점을 추정하지만 답은 아직 모른다.'}]
    public['timelineLanes']=[['EDWARD','서쪽 여행 → 귀환 → 편지 → 이슈발 기도소'],['ALPHONSE','싱에서 보낸 편지 · 현재 정확한 동선은 미공개'],['LING','황제가 된 뒤 · 이슈발 옛길 요청 수신'],['MUSTANG / MILES','재건·조사 권한 문제 제기 · 아직 결론 없음']]
    known=[('전후 재건과 조사 권한','머스탱과 마일즈는 국가의 재건 책임과 이슈발의 결정권을 두고 논의한다.'),('재건 현장과 기도소','에드는 마일즈·스카를 만나 오래된 기도소와 형의 노트를 조사한다.'),('알의 편지와 링의 통치','알이 싱에서 보낸 편지와 링에게 들어온 교역로 요청이 제시됐다. 이후 동선은 미공개다.'),('지도 속 동쪽 사막','싱과 아메스트리스 사이의 사막. 오래된 길의 존재는 요청과 기록의 단서로만 제시됐다.'),('연금술 없이 지식을 쓰는 에드','서쪽 광산 사고를 현지 연금술사와 함께 해결한 프롤로그.'),None,('미확정 질문','관찰된 유사성과 인물의 해석을 구분한다. 문양의 기원과 작동 원리는 아직 밝혀지지 않았다.'),('기도의 문양','에드는 연성진과 닮았다고 하고 스카는 기도라고 설명한다. 동일한 기술인지는 미확정이다.')]
    for record,entry in zip(public['world'],known):
        if entry:record['title'],record['text']=entry
    for c in public['characters']:
        c['change']='공개된 원고 이후의 변화는 작가 전용 자료로 분리되어 있습니다.'
    public['characters'][0]['location']='제2화 시점 · 이슈발 기도소'
    public['characters'][1]['location']='편지에 나타난 싱 · 현재 상세 동선 미공개'
    public['characters'][1]['goal']='에드에게 연단술과 스카 형에 관한 질문을 편지로 전한다.'
    public['principles'][3]['text']='인물의 해석·추측과 작품의 확정 설정을 구분한다. 공개 원고의 미스터리를 성급히 해답으로 바꾸지 않는다.'
    public['chapters'][-1]['title']='미공개 초기 구성 항목'
    public['world'][-1]['en']='Prayer motif'
    public['chapters'][-1]['outline']='초기 구성안의 항목. 공개된 원고에서는 기도소 문양과 연구 노트를 확인한 단계이며 이후 전개는 미공개다.'
    for m in public['mysteries']:m['plannedClues']=[]
    return public,author

def main():
    publish_manuscripts()
    shared=load(ROOT/'site/data/project.json')
    legacy=load(ROOT/'private/archive/pre-master-project.json')
    master=load(ROOT/'private/master-data.json')
    public,author=projections(shared,legacy,master)
    dump(ROOT/'site/data/project.json',public)
    # Same UI assets, different data and server root. Never copy private/ into site/.
    dest=ROOT/'author-site';dest.mkdir(exist_ok=True)
    for name in ['index.html','app.js','core.mjs','style.css','mark.svg']:shutil.copyfile(ROOT/'site'/name,dest/name)
    dump(dest/'data/project.json',author)
    print('Built reader snapshot through episode 2 and isolated author snapshot')
if __name__=='__main__':main()
