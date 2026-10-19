"""One-time reproducible migration from the archived v1 author data."""
from pathlib import Path
import json, re, hashlib
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'private/archive/master-data-v1.json').read_text('utf8'))
text=(ROOT/'private/STORY_MASTER_PLAN_v2.md').read_text('utf8')
p=data['masterPlan']
p.update(id='master-v2',version='2.0',title='Story Master Plan v2.0',sourceFile='private/STORY_MASTER_PLAN_v2.md',fullText=text,sourceHash=hashlib.sha256(text.encode()).hexdigest(),mainQuestion='힘을 가진 사람은 어디까지 결정해야 하는가?',convergence='힘을 얻는다는 것은 더 많은 것을 마음대로 할 수 있게 되는 것이 아니라, 더 많은 것에 책임을 져야 한다는 뜻이다.')
matches=list(re.finditer(r'^(\d+)\. (.+)$',text,re.M))
p['sections']=[{'number':int(m[1]),'title':m[0],'text':text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)].strip()} for i,m in enumerate(matches)]
p['sourcePriority'][1]='Story Master Plan v2.0 · 활성 창작 기준; v1.0과 초기 기획은 이력'
p['arcs']=[
 {'name':'Edward','start':'알을 되찾고 연금술을 포기함','initial':'진리를 본 경험 때문에 이슈발라의 답도 알 수 있다고 믿는다','growth':'오답 가설의 붕괴를 겪으며 모르는 것을 받아들인다','ending':'진리를 본 것과 세상을 아는 것은 다르다'},
 {'name':'Mustang','start':'국가를 바꿀 힘에 가까워짐','initial':'국가가 책임지고 이슈발을 재건해야 한다','growth':'지역 권리와 국가 전체의 책임을 함께 고려한다','ending':'대신 결론을 주거나 방관하지 않고 결정에 참여할 구조를 만든다'},
 {'name':'Miles','start':'이슈발의 결정권을 되찾으려 함','initial':'국가의 책임이 다시 지배할 근거가 되어서는 안 된다','growth':'이슈발 내부에서도 서로 다른 미래를 원함을 마주한다','ending':'자신이 하나의 이슈발의 뜻을 대표한다고 쉽게 말하지 않는다'},
 {'name':'Ling','start':'야오족을 지키고 황제가 됨','initial':'서부 교역의 이익이 야오족과 부족 간 균형에 충돌한다','growth':'야오족을 넘어 모든 부족으로 책임 범위를 넓힌다','ending':'강제 개방 대신 협상 구조를 만들고 에드가 해결해주기 전부터 행동한다'},
 {'name':'Scar','start':'이슈발라의 신앙을 지킴','initial':'형의 연구가 기존 교리를 흔든다','growth':'에드의 구조적 이해와 자신의 신앙적 의미를 함께 마주한다','ending':'신앙과 새로운 지식이 반드시 모순되는 것은 아님을 받아들인다'},
 {'name':'Alphonse','start':'싱에서 동쪽 지식을 배움','initial':'직접 POV는 숨기고 편지와 타인의 언급만 등장한다','growth':'에드와 다른 방향에서 같은 질문을 추적한다','ending':'다시 열린 옛길에서 재회하고 함께 싱으로 걷는다'}]
p['researchPath']=['이슈발라 신앙','고대 이슈발 기록','기도 문양·흐름·순환','동쪽에서 전해진 기록','사라진 동방 교역로','싱의 자연철학','용맥','연단술','아메스트리스 연금술과 비교','역전연성진 연구']
p['forbiddenPromotions'] += ['적맥석의 예시 성질을 전부 확정 설정으로 승격','광물을 흐름의 원인 또는 이슈발라의 정체로 확정','마일즈를 이슈발 전체의 단일한 대변자로 취급','링의 서부 정치 갈등을 에드가 대신 해결','결정권 분배를 권력자의 무결정·책임 회피와 동일시','가칭 A·B부족의 이름·양보선을 임의 확정']
p['roadmap']=p['roadmap'][:2]+[
 {'id':'part-1','label':'PART I · 1~3화','title':'신의 이름','summary':'편지 → 유적·형의 기록 → 이슈발라 → 진리라는 에드의 가설. 1·2화 등록, 3화 집필 전.','status':'PARTIAL','episodeRange':[1,3],'fixed':False},
 {'id':'part-2','label':'PART II · 4~7화 전후','title':'이슈발의 땅','summary':'가설의 모순·연구 출발점·동방 기록 → 유적 조사권 → 전략자원 → 내부 정치 갈등 → 옛길 발견.','status':'PLANNED','episodeRange':[4,7],'fixed':False},
 {'id':'part-3','label':'PART III · 8~11화 전후','title':'사라진 길','summary':'에드·스카의 옛길 추적 → 연단술 습득 경로 최종 규명 → 오답 붕괴 → 용맥 비교 → 경제가치와 양국 정치 문제.','status':'PLANNED','episodeRange':[8,11],'fixed':False},
 {'id':'part-4','label':'PART IV · 12~16화 전후','title':'황제의 나라','summary':'A·B·야오족의 이해충돌 → 링·란팡 서부 원정과 비살상 전투 → 에드·링 재회. 링의 갈등을 에드가 해결하지 않는다.','status':'PLANNED','episodeRange':[12,16],'fixed':False},
 {'id':'part-5','label':'PART V · 17~20화 전후','title':'다시 열린 길','summary':'자원개발·군부·부족 갈등 → 참여와 협상 구조 → 개발권·수익·유산·주둔 조건 합의 → 개방 → 알 공개·형제 재회·에필로그.','status':'PLANNED','episodeRange':[17,20],'fixed':False}]
p['causalChain']=[{'id':f'cause-{i+1:02}','text':s,'state':'원고 제시' if i<4 else '작가 계획 · 미공개'} for i,s in enumerate([
 '알의 편지','스카 형의 연단술 연구에 대한 의문','이슈발 고대 유적 조사','이슈발라의 정체에 대한 의문','고대 이슈발·싱 지식 교류 발견','형이 흔적을 따라 연단술을 연구했음 확인','고대 이슈발·싱 교역로 발견','이슈발 지하 전략자원 발견','교역로의 현대적 경제가치 급상승','자치·자원 소유권 / 국가안보 / 서부 부족 균형','머스탱·마일즈·링의 정치적 선택','누가 어떤 조건으로 길을 여는가','에드와 알의 재회'])]
p['resource']={'id':'resource-provisional','name':'적맥석','nameStatus':'가칭 · 미확정','existence':'이슈발 지하 전략자원 발견은 창작 계획으로 확정 · 작중 미공개','confirmed':['산업적·군사적·연금술적 가치가 높은 희귀 광물','광맥 분포와 고대 기록의 땅의 흐름이 유사'], 'examples':['고온·고압 안정성','특수 합금 제조','철도·기계산업','군수산업','특정 연성의 촉매'],'propertiesStatus':'예시 · 정확한 성질은 추후 확정','hypotheses':['에드가 광물 에너지를 이슈발라로 의심할 수 있음','흐름의 원인이 아니라 환경의 결과물일 가능성'],'hypothesesStatus':'가능성 · 결론 미확정','sourceSections':[7]}
for row in data['disclosureBoard']:row['actualSetting']['source']='master-v2'
byid={r['id']:r for r in data['disclosureBoard']}
byid['reveal-brother']['actualSetting']['text']='신앙·고대 기록 → 동쪽 기록 → 사라진 길 → 싱의 자연철학·용맥·연단술 → 두 체계 비교와 역전연성진 연구.'
byid['reveal-brother']['revealPlan']['stage']='PART II 연구 출발점 → PART III 습득 경로 최종 규명 · 화수 유동'
byid['reveal-route']['actualSetting']['text']='Amestris → Ishval → Desert → Western Xing → Xing Interior. 지식의 길이 전략자원과 시장을 잇는 경제회랑이 되고, 여러 당사자가 조건을 협상한다.'
byid['reveal-route']['revealPlan']['stage']='PART II 옛길 발견 → PART III 경제가치 → PART IV 국제 갈등 → PART V 조건 합의·개방'
for rid in ['reveal-ishvala','reveal-truth']:byid[rid]['revealPlan']['stage']='PART I 오답 확신 → PART II 모순 → PART III 가설 붕괴 → 이후 해석의 여지 유지'
for rid,title,truth,stage in [
 ('reveal-resource','이슈발의 전략자원','이슈발 지하 희귀 전략자원 발견. 명칭 적맥석과 구체 성질은 미정이며 활용 예시는 확정 목록이 아니다.','PART II 발견 → PART III 경제가치 → PART V 개발 조건 협상'),
 ('reveal-mineral-flow','광맥과 땅의 흐름','광맥 분포가 고대 기록과 유사하다. 광물이 흐름의 원인이 아니라 결과물일 수 있다는 해석은 가능성으로 유지한다.','PART II 이후 관찰·가설 · 결론과 화수 미정'),
 ('reveal-representation','누가 당사자를 대표하는가','이슈발 내부·서부 부족 내부도 단일하지 않다. 지도자는 개발권·수익배분·유산·군 주둔·부족 간 분배를 협상할 참여 구조를 만든다.','PART II~IV 이해관계 확대 → PART V 협상 구조·합의')]:
  data['disclosureBoard'].append({'id':rid,'title':title,'asOfEpisode':2,'readerKnowledge':{'text':'2화까지 공개된 원고에는 이 사안이 제시되지 않았다.','evidence':[]},'edHypothesis':{'text':'2화까지 이 사안에 대한 에드의 지식·가설은 제시되지 않았다.','status':'미공개','evidence':[]},'actualSetting':{'text':truth,'kind':'ORIGINAL','source':'master-v2','certainty':'명시한 미정·가능성 구분 유지'},'revealPlan':{'stage':stage,'episode':None,'fixed':False},'readerVisible':False})
# Political fields keep evidence, examples and unset values distinct.
def field(text=None,sections=(),status='명시'):
 return {'text':text,'status':status if text else '미정','sections':list(sections)}
def party(id,name,group,wants=None,fears=None,concedes=None,redlines=None,relations=(),sections=(),example=False):
 return {'id':id,'name':name,'group':group,'kind':'ORIGINAL','source':'master-v2','sections':list(sections),'wants':field(wants,sections),'fears':field(fears,sections),'concedes':field(concedes,sections,'예시' if example else '명시'),'redlines':field(redlines,sections,'예시' if example else '명시'),'relations':[{'target':target,'text':txt,'sections':list(sections)} for target,txt in relations]}
data['politicalBoard']={'version':'2.0','asOf':'작가 계획 · 2화 이후 미공개 포함','source':'master-v2','notice':'원하는 것과 비타협 조건은 별개입니다. 명시되지 않은 두려움·양보선은 미정이며 관계는 고정 동맹을 뜻하지 않습니다.','parties':[
 party('pol-mustang','머스탱','지도자','재건 책임과 국가 산업·안보를 함께 고려하고 실질적인 참여 구조를 만든다',relations=[('pol-miles','이슈발 회복이 목표지만 국가 책임과 결정권을 두고 갈등'),('pol-army','국가안보 논리는 고려하되 국가의 독점 결정과 구분')],sections=[9,19]),
 party('pol-miles','마일즈','지도자','이슈발의 문화·역사·정치적 결정권을 돌려받는다','책임과 재건을 이유로 한 국가의 재지배',relations=[('pol-mustang','목적은 같지만 방법을 두고 갈등'),('pol-development','이슈발 내부에 서로 다른 목소리가 있음을 마주함'),('pol-preservation','자신이 모두를 대표한다고 쉽게 말할 수 없음')],sections=[10]),
 party('pol-ling','링 / 싱 황실','지도자','교역로 개방과 싱 전체를 위한 판단','부족 내전','야오족의 일부 경제적 이익','싱의 통합',relations=[('pol-yao','출신 부족의 이익과 싱 전체에 대한 책임이 충돌'),('pol-a','서부에 직접 가서 협상'),('pol-b','A의 성장에 대한 불안을 고려')],sections=[12,13,14,15,19],example=True),
 party('pol-army','아메스트리스 군부','아메스트리스','국가안보를 위한 유적 조사권과 전략자원 국가 관리','전략자원 공급의 불안정',relations=[('pol-miles','유적 조사권·역사와 자원에 대한 개입 충돌'),('pol-independence','국가 관리와 독립 요구가 충돌')],sections=[9,18]),
 party('pol-development','이슈발 개발파','이슈발','광산·교역 수익으로 학교·병원·주택·상하수도·산업을 만든다',relations=[('pol-preservation','개발과 보존의 조건을 두고 충돌')],sections=[8,18]),
 party('pol-preservation','이슈발 보존파','이슈발','유적·성지와 땅을 보존한다','자원 개발을 통한 또 다른 침탈',redlines='유적과 성지를 파괴해서는 안 된다',relations=[('pol-development','광산 개발 추진과 보존 요구가 충돌'),('pol-army','자원 개발이 국가 침탈로 이어질 수 있음을 우려')],sections=[8,18]),
 party('pol-autonomy','이슈발 자치파','이슈발','자원을 바탕으로 아메스트리스 안에서 강력한 자치권을 확보한다',relations=[('pol-independence','자치와 독립이라는 정치적 목표가 다름')],sections=[8]),
 party('pol-independence','이슈발 독립파','이슈발','자원 수익을 경제 기반으로 독립한다',relations=[('pol-autonomy','국가 내 자치와 분리 독립의 차이'),('pol-army','국가의 자원 관리 요구와 충돌')],sections=[8,18]),
 party('pol-mining','광산지역 주민','지역 당사자',relations=[('pol-development','개발권·수익배분 협상에 참여할 별도 당사자; 개발파와 동일시하지 않음')],sections=[3,19]),
 party('pol-religious','종교 지도자','지역 당사자',relations=[('pol-preservation','문화유산 보호 협상 참여; 보존파와 동일시하지 않음')],sections=[19]),
 party('pol-a','A부족 · 가칭','싱 서부','영토 통과에 따른 통행·운송·창고·가공·무역의 경제적 권리',relations=[('pol-b','역사적 경쟁관계; 교역로가 세력균형을 바꿈'),('pol-yao','A의 성장은 야오족의 상대 영향력을 줄일 수 있음'),('pol-chief','족장은 협상 가능'),('pol-armed','내부 젊은 무장세력은 황실 개입을 거부')],sections=[12,13,15,18]),
 party('pol-b','B부족 · 가칭','싱 서부','A부족의 교역로 독점을 받아들일 수 없다','황제가 A부족을 키워 자신들을 견제한다는 의심',relations=[('pol-a','역사적 경쟁관계'),('pol-ling','황제 정책의 편파성을 의심')],sections=[13,18]),
 party('pol-yao','야오족','싱','야오족 보호와 영향력 유지','A의 성장과 링의 정책으로 상대 영향력이 약화될 수 있음',relations=[('pol-ling','황제의 출신 부족; 국가 전체의 이익과 충돌할 수 있음'),('pol-a','교역로 개방으로 세력균형 변화')],sections=[13,14,18]),
 party('pol-desert','사막 지역민','지역 당사자','삶의 터전이 국제교역로로 바뀌는 것에 저항','유목생활·문화·부족경제·기존 관계의 변화',relations=[('pol-ling','국제교역로 협상에 참여하는 당사자')],sections=[15,18,19]),
 party('pol-chief','서부 부족 족장','싱 서부','협상 가능; 구체 조건은 미정',relations=[('pol-armed','같은 부족 내부에서도 황실 개입에 대한 의견이 다름'),('pol-ling','협상 상대')],sections=[15]),
 party('pol-armed','젊은 무장세력','싱 서부','황실 개입을 거부한다','돈이 생기자 찾아온 황실과 지역생활의 변화',relations=[('pol-chief','협상 가능한 족장과 의견이 갈림'),('pol-ling','링 일행 습격; 링은 자신의 백성으로 보고 비살상을 명령')],sections=[15])
 ],'negotiation':{'participants':['이슈발 대표','광산지역 주민','종교 지도자','아메스트리스 정부','싱 황실','A부족','B부족','사막 지역민'],'topics':['자원개발권','수익배분','교역로 관리','문화유산 보호','군대 주둔 제한','부족 간 경제배분'],'status':'협상 구조 형성은 확정된 창작 방향 · 구체 수치·제도·조건은 미정','sections':[19]},'openQuestions':[
 '어떤 기준으로 대표를 선정하며 내부 이견을 어떻게 반영할 것인가',
 '명시되지 않은 세력별 양보선·비타협 조건',
 '구체적인 자원개발권·수익배분 비율·주둔 제한과 집행 방식',
 '적맥석의 정식 명칭·성질과 기존 운송로보다 새 길이 유리한 이유']}
ling=next(r for r in data['politicalBoard']['parties'] if r['id']=='pol-ling')
ling['fears']['status']='예시'
for key in ['fears','concedes','redlines']:ling[key]['reference']='Political Board 추가 지침 · 링 예시'
a=data['masterAlignment'];a['title']='Story Master Plan v2.0 대비 점검'
a['basis']='프롤로그~2화 / v1.0과 초기 기획 / v2.0 마스터 플랜'
a['findings'][0].update(planQuote='마지막에 다시 열린 옛길에서 둘이 만난다.',reason='초기 중반 싱 합류는 v2에서도 채택하지 않는다. 마지막 옛길 재회와 알 POV 비공개를 활성 기준으로 유지한다.')
a['findings'][1]['planQuote']='스카 형이 어떻게 연단술에 도달했는지 최종적으로 밝혀짐.'
a['findings'][1]['action']='2화는 잠정 가설로 읽히게 하거나 노트 순서의 근거를 보강한다. PART II의 출발점 규명과 PART III의 최종 경로 회수를 구분한다. 원고는 자동 수정하지 않는다.'
a['findings'][2].update(title='서부 국경의 링 재회와 마지막 형제 재회',state='v2에서 동선 구체화 · 상세 위치 추적',planQuote='에드가 싱에 가까워지면서 소문을 듣는다.',reason='v2는 링을 서부로 이동시켜 에드가 싱 내륙에 먼저 들어갔다가 돌아와야 하는 필요를 줄였다. 하지만 링과의 재회 위치·알과의 최종 재회 위치·두 사건의 시간차는 아직 미정이다.',action='서부 국경과 옛길을 기준으로 위치를 기록한다. 미정 왕복 사건을 만들지 않는다.')
a['findings'][3].update(planQuote='고대 교역로의 싱 측 입구는 서부 국경의 특정 부족 영토에 있다.',reason='v2에서 입구와 핵심 정치 갈등이 싱 서부로 구체화됐다. 1화의 동부 부족 대표가 서쪽 상인 문제를 전달하는 이유는 아직 없다. 상업 이해관계일 수 있으므로 단순 방위 오류로 확정하지 않는다.')
a['findings'] += [
 {'id':'ma06','severity':'중간','category':'인과·발견 순서','title':'교역로 발견과 전략자원 발견의 순서','state':'기획 내 순서 미정','evidence':[],'planQuote':'고대 이슈발-싱 교역로 발견 → 이슈발 지하의 전략자원 발견','reason':'2절의 인과관계는 교역로가 먼저지만 23절 PART II는 전략자원을 발견한 뒤 마지막에 옛길을 발견한다. 길의 흔적과 실제 경로 확인을 구분하는 방식은 가능하지만 아직 확정되지 않았다.','action':'두 순서를 병기하고 작가 확정 전 자동으로 하나를 선택하지 않는다.'},
 {'id':'ma07','severity':'중간','category':'경제적 설득력','title':'자원이 새 교역로의 가치를 높이는 근거','state':'후속 집필 전 구체화','evidence':[],'planQuote':'고고학적 발견이 국제정치 문제로 변한다.','reason':'희소성·수요·채굴 가능성과 운송비·기존 길 대비 이점이 아직 수치나 사건으로 정해지지 않았다. 정밀한 경제 모델은 필요 없지만 새 길이 필요한 이유는 보여줘야 한다.','action':'적맥석 성질 예시를 모두 확정하지 않고, 작가가 고른 성질과 운송 조건을 나중에 근거로 등록한다.'},
 {'id':'ma08','severity':'중간','category':'대표권·결말','title':'협상 참여자를 정하는 절차 자체도 검토 대상','state':'v1 결말 대체 · 제도 세부 미정','evidence':[],'planQuote':'누가 결정해야 하는지를 정하는 것 역시 권력자의 책임이다.','reason':'v1의 지도자 양보와 단순한 지역 결정만으로 끝나지 않는다. 마일즈 한 사람을 이슈발 대표로 놓거나, 같은 부족을 단일한 의견으로 취급하면 v2의 주제에 어긋난다.','action':'참여 집단과 협상 의제를 등록하되 대표 선정·합의·집행 제도는 미정으로 유지한다.'}
 ]
a['checks'] += [{'title':'자원 발견 이전의 2화 조사권 갈등은 v2의 갈등 씨앗으로 유지 가능','evidence':[],'note':'이미 제시된 재건·문화유산 조사권 문제를 이후 자원·소유권 갈등이 확대한다. 2화에 광물을 소급 삽입하지 않는다.'}]
(ROOT/'private/master-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf8')
print('Prepared master v2: 23 sections, 5 parts, 6 arcs, 16 political parties')
