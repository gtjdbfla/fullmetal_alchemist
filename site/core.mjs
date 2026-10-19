export const MYSTERY_STATES=['UNSOLVED','CLUE FOUND','PARTIALLY SOLVED','SOLVED'];
export const CHAPTER_STATES=['IDEA','OUTLINE','DRAFT','COMPLETE','THREADS'];
export const LOCAL_VERSION=1;
export function evidenceParagraph(text,quote){
 const paragraphs=text.split(/\n\s*\n/).slice(1),parts=quote.split(/\n\s*\n/);
 const index=paragraphs.findIndex((_,i)=>parts.every((part,j)=>paragraphs[i+j]?.includes(part)));
 return index<0?0:index+1;
}
export function blankWorkspace(){return {version:LOCAL_VERSION,notes:{},mysteries:{},chapters:{},reviews:{},manuscripts:[]};}
export function validateWorkspace(value,project){
 if(!value||value.version!==LOCAL_VERSION)throw new Error('지원하지 않는 작업함 버전입니다');
 const out=blankWorkspace();
 for(const key of ['notes','mysteries','chapters','reviews']){
  if(!value[key]||typeof value[key]!=='object'||Array.isArray(value[key]))throw new Error('작업함 구조가 올바르지 않습니다');
 }
 const ids=new Set(['world','characters','mysteries','chapters','reviews'].flatMap(k=>project[k].map(x=>x.id)));
 for(const party of project.politicalBoard?.parties||[])ids.add(party.id);
 for(const [key,v] of Object.entries(value.notes)){if(!ids.has(key)||typeof v!=='string'||v.length>20000)throw new Error('메모 항목이 올바르지 않습니다');out.notes[key]=v;}
 for(const [key,v] of Object.entries(value.mysteries)){if(!project.mysteries.some(x=>x.id===key)||!MYSTERY_STATES.includes(v.status)||typeof v.evidence!=='string'||v.evidence.length>20000)throw new Error('미스터리 항목이 올바르지 않습니다');if(v.status==='SOLVED'&&!v.evidence.trim())throw new Error('회수 완료에는 원고 근거가 필요합니다');out.mysteries[key]={status:v.status,evidence:v.evidence};}
 for(const [key,v] of Object.entries(value.chapters)){if(!project.chapters.some(x=>x.id===key)||!CHAPTER_STATES.includes(v))throw new Error('챕터 상태가 올바르지 않습니다');out.chapters[key]=v;}
 for(const [key,v] of Object.entries(value.reviews)){if(!project.reviews.some(x=>x.id===key)||!['OPEN','REVIEWED'].includes(v))throw new Error('검토 상태가 올바르지 않습니다');out.reviews[key]=v;}
 if(!Array.isArray(value.manuscripts)||value.manuscripts.length>100)throw new Error('원고 목록이 올바르지 않습니다');
 for(const m of value.manuscripts){if(!project.chapters.some(x=>x.id===m.chapter)||typeof m.text!=='string'||!m.text.trim()||m.text.length>100000||typeof m.savedAt!=='string'||!Number.isFinite(Date.parse(m.savedAt)))throw new Error('원고가 올바르지 않습니다');out.manuscripts.push({chapter:m.chapter,text:m.text,savedAt:m.savedAt});}
 return out;
}
export function metrics(project,local){
 const drafts=local.manuscripts.length;
 const statuses=project.mysteries.map(m=>local.mysteries[m.id]?.status||m.status);
 const solved=statuses.filter(s=>s==='SOLVED').length;
 return {registeredManuscripts:(project.manuscripts||[]).length,registeredCharacters:(project.manuscripts||[]).reduce((sum,m)=>sum+m.characters,0),manuscripts:drafts,chaptersWithDraft:new Set(local.manuscripts.map(m=>m.chapter)).size,openMysteries:statuses.filter(s=>s!=='SOLVED').length,solved,reviewed:project.reviews.filter(x=>local.reviews[x.id]==='REVIEWED').length,reviewTotal:project.reviews.length,canonTotal:project.world.filter(x=>x.kind==='CANON').length,canonVerified:project.world.filter(x=>x.kind==='CANON'&&x.canonEvidence).length};
}
export function scanExpressions(text){
 // Literal expression candidates only. Never claims semantic contradiction or AI review.
 const rules=[{id:'alchemy',label:'에드의 능력에 관한 표현',pattern:/에드[^\n。.!?]{0,35}(연금술|연성|손뼉)/g,reason:'에드의 연금술을 되돌리지 않는 원칙과 문맥을 대조하세요. 부정·회상·타인의 행동이면 충돌이 아닐 수 있습니다.'},{id:'identity',label:'진리와 신앙의 동일성 표현',pattern:/(진리[^\n。.!?]{0,40}이슈발라|이슈발라[^\n。.!?]{0,40}진리)/g,reason:'인물의 가설인지 서술자의 확정인지 확인하세요. 동일성을 자동으로 판정하지 않습니다.'},{id:'newpower',label:'새 능력·부활 관련 표현',pattern:/(부활|새로운 능력|제2의 문|제3의 문|연금술이 돌아)/g,reason:'새로운 설정인지 비유인지 확인하고 출처와 확정 상태를 기록하세요.'}];
 const found=[];
 for(const rule of rules)for(const match of text.matchAll(rule.pattern)){const index=match.index;found.push({id:rule.id,line:text.slice(0,index).split('\n').length,quote:text.slice(Math.max(0,index-30),Math.min(text.length,index+match[0].length+60)),label:rule.label,reason:rule.reason});if(found.length>=50)return found;}
 return found.sort((a,b)=>a.line-b.line);
}
