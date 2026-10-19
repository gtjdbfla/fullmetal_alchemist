"""Apply the author's nine approved decisions; archived sources remain unchanged."""
from pathlib import Path
import json, re, hashlib
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text('utf8'))
def dump(p,v):(ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf8')
data=load('private/archive/master-data-v2.json');p=data['masterPlan']
decisions=(ROOT/'private/STORY_DECISIONS_v2.1.md').read_text('utf8')
source=(ROOT/'private/STORY_MASTER_PLAN_v2.md').read_text('utf8').replace('Story Master Plan v2.0','Story Master Plan v2.1')
source=source.replace('고대 이슈발-싱 교역로 발견\n↓\n이슈발 지하의 전략자원 발견\n↓\n고대 교역로의 현대적 경제가치 급상승','옛길의 존재를 기록에서 발견\n↓\n이슈발 지하의 전략자원 발견\n↓\n옛길의 실제 경로 확인\n↓\n고대 교역로의 현대적 경제가치 재발견')
start=source.index('※ 명칭과 정확한 성질은 추후 확정.')
end=source.index('그리고 중요한 특징이 있다.',start)
source=source[:start]+'''※ 명칭은 가칭이다. 핵심 용도는 확정하고 정확한 성분·물성 수치는 미정으로 둔다.

적맥석은 극한의 열과 압력을 견디는 합금의 핵심 소재다.
증기기관·대형 기계·철도·군수산업에 중요해질 수 있다.
만능 광물로 만들거나 별도의 연금술 특수능력을 부여하지 않는다.
싱에는 수요가 있으나 대규모 산지가 부족하다.

고대 이슈발 사람들은 이미 이 돌을 알고 현대 산업과는 다른 용도로 사용했다.
에드는 유적을 조사하다 붉은 광물을 역사적 단서로 발견하고, 이후 분석으로 특이한 물성을 확인한다.
기도소·의식 장소의 소량 사용과 구체 대사는 예시이며 정식 장면은 미정이다.

'''+source[end:]
source=source.replace('따라서 고고학적 발견이 국제정치 문제로 변한다.','''기존 운송 경로는 이슈발 → 아메스트리스 내륙 → 기존 국제교역망 → 우회 → 싱이다.
옛길은 이슈발 → 사막 → 싱 서부로 연결된다.
대량의 무거운 광물을 운송할 때 옛길의 효율이 압도적으로 높다.
정확한 운임·거리·운송수단·상업 개통 일정은 미정이다.
에드는 지식의 길을 찾고, 이후 다른 당사자들이 경제적 가치를 발견한다.
따라서 고고학적 발견이 국제정치 문제로 변한다.''')
source=source.replace('마지막에 다시 열린 옛길에서 둘이 만난다.','''에드는 이슈발 → 고대 교역로 → 사막 → 싱 서부 국경 → A부족 영역으로 이동하고 여기서 링과 재회한다.
링은 이미 A/B부족 문제로 서부에 와 있으며 에드를 만나러 온 것이 아니다.
에드는 일정 부분 동행한 뒤 합의 이후에도 계속 동쪽으로 움직인다.
마지막에 새로 열린 옛길의 싱 측 구간에서 반대 방향으로 조사해 오던 알과 만난다.
에드는 서쪽으로 되돌아가지 않는다.''')
source=source.replace('편지와 다른 사람의 언급만 등장한다.','편지와 다른 사람의 언급만 등장한다. 이동 흔적은 계속 노출하되 발견 내용은 공개하지 않는다. Al Trail로 발신·수신·위치와 공개 범위를 추적한다.')
source=source.replace('마지막에 동쪽으로 이어지는 옛길 발견.','옛길의 존재를 기록에서 먼저 확인하고 전략자원을 발견한다. 실제 경로 확인은 PART III에서 진행한다.')
source=source.replace('에드와 스카가 옛길을 추적.','에드와 스카가 옛길을 추적하고 실제 경로를 확인한다. 이후 경제적 가치가 재발견된다.')
source+='\n\n작가 확정 추가 결정 · v2.0의 미정·충돌 표현보다 우선\n\n'+decisions
(ROOT/'private/STORY_MASTER_PLAN_v2.1.md').write_text(source,'utf8')
p.update(id='master-v2.1',version='2.1',title='Story Master Plan v2.1',sourceFile='private/STORY_MASTER_PLAN_v2.1.md',sourceHash=hashlib.sha256(source.encode()).hexdigest(),fullText=source)
# Parse the original 23 sections separately; approved addendum has its own rendering.
base=source.split('\n\n작가 확정 추가 결정')[0]
matches=list(re.finditer(r'^(\d+)\. (.+)$',base,re.M))
p['sections']=[{'number':int(m[1]),'title':m[0],'text':base[m.end():matches[i+1].start() if i+1<len(matches) else len(base)].strip()} for i,m in enumerate(matches)]
p['sourcePriority'][1]='Story Master Plan v2.1 · 확정 결정이 v2.0의 미정·충돌 표현보다 우선'
p['decisionSource']={'file':'private/STORY_DECISIONS_v2.1.md','text':decisions,'sha256':hashlib.sha256(decisions.encode()).hexdigest()}
p['route']=['이슈발','고대 교역로','사막','싱 서부 국경','A부족 영역','새로 열린 길의 싱 측 구간','함께 싱으로']
p['resource'].update(existence='고대 이슈발이 이미 알고 다른 용도로 사용한 돌을 에드가 유적 조사 중 발견하고, 이후 분석으로 산업적 물성을 확인한다.',confirmed=['극한의 열과 압력을 견디는 합금의 핵심 소재','싱에는 수요가 있지만 대규모 산지가 부족함','고대 이슈발 문화에서 사용한 돌 · 현대 산업 용도와 구분','광맥 분포와 고대 기록의 땅의 흐름이 유사'],examples=['증기기관·대형 기계·철도·군수산업의 활용 가능성'],propertiesStatus='핵심 용도 확정 · 성분·물성 수치·개별 활용은 미정',transport={'existing':'이슈발 → 아메스트리스 내륙 → 기존 국제교역망 → 우회 → 싱','new':'이슈발 → 사막 → 싱 서부','advantage':'무거운 광물의 대량 운송에서 옛길이 압도적으로 효율적','unknowns':'정확한 거리·운임·운송수단·상업 개통 일정 미정'},excluded=['연금술 촉매 등 별도의 특수능력','모든 산업 문제를 해결하는 만능 광물'],perspectives=[{'name':n,'meaning':v} for n,v in [('에드','연구대상'),('스카','문화·신앙'),('마일즈','이슈발의 유산'),('머스탱','정치적 책임'),('군부','전략자원'),('상인','돈'),('링','국가경제'),('A부족','지역발전')]])
p['causalChain']=[{'id':f'cause-{i+1:02}','text':s,'state':'원고 제시' if i<4 else '작가 확정 · 미공개'} for i,s in enumerate(['알의 편지','스카 형의 연단술 연구 의문','이슈발 유적 조사','이슈발라의 정체 의문','동쪽 지식 교류·옛길의 존재를 기록에서 확인','고대 문화의 붉은 돌을 역사적 단서로 발견','분석으로 전략자원의 산업적 가치 확인','에드가 옛길의 실제 경로 확인·연단술 유입 경로 규명','옛길의 경제적 가치 재발견','자치·소유권 / 안보 / 부족 균형 갈등','머스탱·마일즈·링의 정치적 선택','참여 구조와 개방 조건 합의','동쪽으로 가는 에드와 서쪽으로 오는 알의 재회'])]
p['forbiddenPromotions']=[x for x in p['forbiddenPromotions'] if '성질을 전부' not in x]+['옛길 기록·실제 경로 확인·대량 운송망 개통을 같은 사건으로 취급','알의 이동 흔적 예시를 이미 등장한 원고로 취급','에드의 동선을 서쪽으로 되돌림','마일즈를 이슈발 전체의 대표로 확정','교역로 탐색의 최초 동기를 광물 운송으로 바꿈']
for r in p['roadmap']:
 if r['id']=='part-2':r['summary']='2화 가설의 증거 축적 → 옛길 존재의 기록 → 문화 속 붉은 돌과 산업적 물성 발견 → 조사권·유산·개발 갈등. 실제 경로는 아직 확인 전.'
 if r['id']=='part-3':r['summary']='에드·스카가 실제 옛길 확인 → 연단술 유입 경로 최종 규명 → 오답 붕괴 → 용맥 비교 → 운송 우위와 경제적 가치 재발견.'
 if r['id']=='part-4':r['summary']='링은 A/B부족 문제로 먼저 서부에 와 협상·비살상 전투를 겪는다. 동쪽으로 가던 에드와 A부족 영역에서 재회하며 일정 부분 동행한다.'
 if r['id']=='part-5':r['summary']='다양한 이슈발 입장과 각 당사자 참여 → 조건 협상·옛길 개방 → 에드는 계속 동쪽으로 이동 → 싱 측 구간에서 알과 최종 재회. 대표 선출·협정 세부는 후반 집필 전 설계.'
data['politicalBoard']['version']='2.1'
data['politicalBoard']['negotiation']['status']='서로 다른 입장 참여 원칙 확정 · 대표 선출과 협정 세부는 후반 집필 전 설계'
data['politicalBoard']['openQuestions']=['대표 선출 방법과 협정 구조 · 후반 집필 전 설계','명시되지 않은 세력별 양보선·비타협 조건','적맥석 정식 명칭·수치·분석 방법과 고대 사용의 구체 장면','운송 거리·운임·수단·시설·상업 개통 일정']
for r in data['politicalBoard']['parties']:
 r['source']='master-v2.1'
 if r['id']=='pol-miles':r['wants']['text']='이슈발의 결정권 회복을 연결하되 자신을 전체의 대표로 취급하지 않는다'
p['arcs'][2]['ending']='중요한 당사자이자 연결자로 남고, 서로 다른 이슈발 내부 입장이 실제 협상에 참여하도록 한다'
p['arcs'][-1]['ending']='이동 흔적은 남기고 발견은 숨긴다. 최종부 싱 측 구간에서 에드와 만난다'
# Explicit manuscript edits, preserving previous published versions.
one=(ROOT/'manuscripts/archive/001-eastbound.v2.md').read_text('utf8')
one=one.replace('폐하. 동부 부족 대표들이 도착했습니다.','폐하. 서부 국경지역 대표들이 도착했습니다.')
(ROOT/'manuscripts/001-eastbound.md').write_text(one,'utf8')
two=(ROOT/'manuscripts/archive/002-name-of-god.v1.md').read_text('utf8')
start=two.index('그런데 이상했다.\n\n에드는 앞쪽으로 다시 돌아갔다.')
end=two.index('방 안이 조용해졌다.',start)
old=two[start:end]
approved=decisions.split('승인된 교체 대화:\n\n')[1].split('\n\n기존 원고에서')[0]
retained=two[two.index('에드가 노트를 펼쳐 보였다.',start):two.index('에드의 표정에서 흥분이 사라졌다.',start)]
new=approved+'\n\n'+retained
two=two[:start]+new+two[end:]
(ROOT/'manuscripts/002-name-of-god.md').write_text(two,'utf8')
proof=load('docs/PROOFREADING.json')
proof['checked']=['프롤로그 v1','제1화 v3','제2화 v2']
proof['corrections']=proof['corrections'][:1]+[
 {'manuscript':'ms-001-v1','fromVersion':2,'toVersion':3,'before':'폐하. 동부 부족 대표들이 도착했습니다.','after':'폐하. 서부 국경지역 대표들이 도착했습니다.','reason':'사용자 확정: 싱 정치 갈등의 서부 국경 설정에 맞춘 교정','originalFile':'manuscripts/archive/001-eastbound.v2.md'},
 {'manuscript':'ms-002-v1','fromVersion':1,'toVersion':2,'before':old.strip(),'after':new.strip(),'reason':'사용자 승인 대화로 연구 경로의 확정 → 유력한 가설. 원의 방향·땅·순환·흐름 단서는 유지','originalFile':'manuscripts/archive/002-name-of-god.v1.md'}]
dump('docs/PROOFREADING.json',proof)
review=load('docs/STORY_REVIEW.before-v2.1.json');review['id']='review-episode-002-v2'
f=next(f for f in review['findings'] if f['id']=='a02')
f.update(title='연구 순서 단정 → 가설로 교정 완료',severity='참고',verdict='수정 완료 · 최종 경로는 아직 미회수',evidence=[{'manuscript':'ms-002-v1','quote':'반대였을지도 몰라.'}],reason='승인된 교체 대화는 노트 배열을 관찰 근거로 삼되 연구 경로를 단정하지 않는다. 현재 원고에 제시된 것은 가설이며 연단술 유입 경로의 증명은 남아 있다.',suggestion='후속 원고에서 증거를 쌓고 경로를 확인한다. 가설 표현의 교정이 미스터리 회수 완료를 뜻하지 않는다.',state='RESOLVED')
review['summary']='1화 부족 방향과 2화 연구 순서의 확정 표현을 사용자 승인에 따라 교정했다. 연구 경로는 여전히 가설이며 혈통 비율·새 노트 관계·방문 시점·출입 절차·서술 시점 검토는 남아 있다.'
dump('docs/STORY_REVIEW.json',review)
quote='반대였을지도 몰라.'
for r in data['disclosureBoard']:
 r['actualSetting']['source']='master-v2.1'
 if r['id']=='reveal-brother':
  r['readerKnowledge']={'text':'기도 문양이 연단술 기록보다 먼저 반복된다는 관찰과, 이슈발 기록에서 연구가 시작됐을 수 있다는 에드의 가설이 제시됐다.','evidence':[{'manuscript':'ms-002-v1','quote':quote}]}
  r['edHypothesis']={'text':'이슈발 기록에서 출발했을 가능성을 제시한다. 연구의 실제 시간 순서와 유입 경로는 아직 확인하지 않았다.','status':'유력한 가설 · 미확정','evidence':[{'manuscript':'ms-002-v1','quote':quote}]}
 if r['id']=='reveal-route':
  r['actualSetting']['text']='옛길의 기록 → 전략자원 → 에드의 실제 경로 확인 → 경제적 가치 재발견. 최초 동기는 지식 추적이며 운송 계획이 아니다.'
  r['revealPlan']['stage']='PART II 옛길 기록·자원 → PART III 실제 경로 확인·경제적 가치 → PART IV 국제 갈등 → PART V 개방'
 if r['id']=='reveal-resource':r['actualSetting']['text']='고대 문화에서 이미 쓰던 붉은 돌을 유적 조사로 발견하고 분석한다. 극한 열·압력 합금의 핵심 소재이며 싱 수요와 대규모 산지 부족, 옛길의 대량 운송 우위가 경제 갈등을 만든다. 특수능력은 없다.'
 if r['id']=='reveal-representation':r['actualSetting']['text']='마일즈는 이슈발 전체 대표가 아닌 당사자·연결자다. 서로 다른 내부 입장이 협상에 참여한다. 대표 선출과 협정 세부는 후반 집필 전에 설계한다.'
data['disclosureBoard'].append({'id':'reveal-al-trail','title':'Al Trail · 알의 이동 흔적','asOfEpisode':2,'readerVisible':False,'readerKnowledge':{'text':'알이 싱에서 편지를 보냈다는 사실만 공개됐다. 서쪽으로 이동 중이라는 정보는 아직 원고에 없다.','evidence':[{'manuscript':'ms-001-v1','quote':'싱으로 떠난 뒤 알은 비교적 꾸준히 소식을 보내왔다.'}]},'edHypothesis':{'text':'편지의 질문을 받고 이슈발로 향했다. 알의 서쪽 이동을 알아챘다는 장면은 아직 없다.','status':'일부 정보만 공개','evidence':[]},'actualSetting':{'text':'알은 반대편에서 같은 길을 조사한다. POV와 발견 내용은 숨기고 이동 흔적은 지속 노출한다. 직접 재등장은 최종부 싱 측 옛길 구간이다.','kind':'ORIGINAL','source':'master-v2.1','certainty':'원칙 확정 · 개별 편지·날짜·대사는 미정'},'revealPlan':{'stage':'중간 편지·타인 언급 → 최종부 역방향 조사와 재회 공개','episode':None,'fixed':False}})
data['alTrail']={'rule':'POV·발견 내용은 비공개, 존재·이동 흔적은 지속 노출','reunion':'에드 동진 / 알 서진 · 최종부 열린 옛길의 싱 측 구간','entries':[
 {'id':'al-existing-letter','status':'원고 제시','stage':'1·2화','origin':'싱 · 세부 도시·발신일 미상','sentAt':None,'receivedAt':None,'readerKnowledge':'싱에서 연단술을 배우며 형에게 질문한 편지','edKnowledge':'편지를 읽고 연구 경로에 의문을 가짐','hidden':'알의 실제 이동 방향과 발견은 아직 공개되지 않음','evidence':[{'manuscript':'ms-001-v1','quote':'싱으로 떠난 뒤 알은 비교적 꾸준히 소식을 보내왔다.'}]},
 {'id':'al-capital-example','status':'예시 · 미집필','stage':'중간 · 화수 미정','origin':'싱 수도 발신 편지 · 후보','sentAt':None,'receivedAt':None,'readerKnowledge':'출발 위치의 기준점 후보','edKnowledge':'정식 장면 없음','hidden':'발견 내용 미공개','evidence':[]},
 {'id':'al-west-example','status':'예시 · 미집필','stage':'중간 · 화수 미정','origin':'서부 어느 도시 발신 · 후보','sentAt':None,'receivedAt':None,'readerKnowledge':'서쪽 이동 흔적 후보','edKnowledge':'서쪽 발신지를 알아차릴 수 있음 · 대사 예시만 있음','hidden':'실제 조사 성과 미공개','evidence':[]},
 {'id':'al-delay-example','status':'예시 · 미집필','stage':'중간 · 화수 미정','origin':'몇 주 늦은 편지 · 지연 이유 미정','sentAt':None,'receivedAt':None,'readerKnowledge':'이동·전달 지연의 흔적 후보','edKnowledge':'정식 장면 없음','hidden':'임의 날짜·도시·지연 이유를 만들지 않음','evidence':[]},
 {'id':'al-mei-example','status':'예시 · 미집필','stage':'중간 · 화수 미정','origin':'메이의 조사 중 부재 언급 · 후보','sentAt':None,'receivedAt':None,'readerKnowledge':'알이 움직이고 있음을 알림','edKnowledge':'누가 언급을 듣는지는 미정','hidden':'POV와 발견 내용 미공개','evidence':[]}], 'checks':['발신지·날짜·수신 시점이 서진 동선과 맞는가','독자는 이동을 알아도 발견 내용까지 알게 되지는 않는가','최종 재회 때 앞선 흔적을 되짚을 수 있는가']}
items=[
 ('발견 순서','확정','옛길 기록 → 전략자원 → 실제 경로 확인 → 경제적 가치','기록과 실물 경로 확인을 구분하며 에드의 탐색 동기는 지식이다.'),
 ('2화 에드 확신','수정 완료','확정 표현을 승인된 가설 대화로 교정','제2화 v2에 반영. PART II 증거 축적, PART III 경로 최종 규명.'),
 ('링·알 동선','확정','에드는 끝까지 서→동, 되돌아가지 않음','A부족 영역에서 이미 서부에 있던 링과 재회. 합의 후 싱 측 옛길 구간에서 알과 만남.'),
 ('1화 동부 부족','수정 완료','서부 국경지역 대표로 교정','제1화 v3에 반영. 불필요한 동부 이해관계를 만들지 않음.'),
 ('알 복선','확정','POV·발견은 숨기고 이동 흔적은 지속 노출','Al Trail에 기존 편지와 미집필 예시를 분리. 날짜·도시·화수는 미정.'),
 ('적맥석 경제성','확정','극한 열·압력 합금 소재 + 싱 수요·산지 부족 + 운송 우위','핵심 용도 확정. 만능 광물·연금술 특수능력 제외. 물성 수치와 운송망 세부는 미정.'),
 ('협상 대표','세부 보류','마일즈 ≠ 이슈발 전체 대표','서로 다른 내부 입장의 참여는 고정. 대표 선출·협정 구조는 후반 집필 전 설계.'),
 ('알 중반 합류','폐기 완료','직접 재등장은 최종부','중반에는 이동 흔적을 남기되 합류하거나 POV를 열지 않음.'),
 ('자원 발견 개연성','확정','고대 문화 속 붉은 돌 → 유적 조사 → 분석 → 산업적 가치','같은 물질을 유산과 자원으로 다르게 보는 갈등. 정확한 의식·분석 장면은 예시·미정.')]
data['storyDecisions']=[{'id':f'decision-{i+1:02}','number':i+1,'title':t,'status':s,'decision':d,'detail':detail,'source':'master-v2.1'} for i,(t,s,d,detail) in enumerate(items)]
checks=data['masterAlignment']['checks']
data['masterAlignment']={'title':'확정 결정 v2.1 · 검토 9항목 처리 결과','basis':'사용자가 확정한 9개 결정 / 제1화 v3·제2화 v2','findings':[{'id':f'decision-review-{r["number"]:02}','severity':'보류' if r['status']=='세부 보류' else '처리됨','category':'작가 결정','title':f'{r["number"]}. {r["title"]}','state':r['status'],'planQuote':r['decision'],'reason':r['detail'],'action':'미정 세부는 후반 설계까지 유지' if r['status']=='세부 보류' else '활성 기준에 반영 · 장면 집필·떡밥 회수 완료와 별도','evidence':([{'manuscript':'ms-002-v1','quote':quote}] if r['number']==2 else [{'manuscript':'ms-001-v1','quote':'폐하. 서부 국경지역 대표들이 도착했습니다.'}] if r['number']==4 else [])} for r in data['storyDecisions']],'checks':checks}
dump('private/master-data.json',data)
print('Applied nine decisions and approved manuscript corrections; previous sources preserved')
