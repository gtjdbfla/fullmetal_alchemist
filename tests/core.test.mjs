import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {blankWorkspace,validateWorkspace,metrics,scanExpressions,evidenceParagraph} from '../site/core.mjs';
const project=JSON.parse(readFileSync(new URL('../site/data/project.json',import.meta.url),'utf8'));
test('public submissions and browser drafts are counted separately',()=>{const m=metrics(project,blankWorkspace());assert.equal(m.manuscripts,0);assert.equal(m.registeredManuscripts,3);assert.equal(m.solved,0);assert.equal(m.openMysteries,16);assert.equal(m.canonVerified,0);});
test('all source records have unique ids',()=>{const rows=['world','characters','mysteries','chapters','reviews'].flatMap(k=>project[k]);assert.equal(new Set(rows.map(r=>r.id)).size,rows.length);assert.ok(rows.every(r=>r.source));});
test('solved mysteries require evidence',()=>{const value=blankWorkspace();value.mysteries.m01={status:'SOLVED',evidence:''};assert.throws(()=>validateWorkspace(value,project),/근거/);value.mysteries.m01.evidence='01화 실제 회수 구절';const normalized=validateWorkspace(value,project);assert.equal(metrics(project,normalized).solved,1);});
test('untrusted imported keys are rejected',()=>{const value=blankWorkspace();value.notes.unknown='x';assert.throws(()=>validateWorkspace(value,project));const injected=blankWorkspace();injected.chapters.ch01='anything';assert.throws(()=>validateWorkspace(injected,project));});

test('political review notes survive author export but are rejected by the reader workspace',()=>{
 const author=JSON.parse(readFileSync(new URL('../author-site/data/project.json',import.meta.url),'utf8'));
 const value=blankWorkspace();value.notes['pol-b']='양보선은 작가 미정으로 유지';
 assert.equal(validateWorkspace(JSON.parse(JSON.stringify(value)),author).notes['pol-b'],value.notes['pol-b']);
 assert.throws(()=>validateWorkspace(value,project));
 assert.throws(()=>validateWorkspace({...value,notes:{'pol-invented':'임의 세력'}},author));
});
test('manuscript versions preserve original text',()=>{const value=blankWorkspace();value.manuscripts.push({chapter:'ch01',text:'첫 줄\n둘째 줄',savedAt:'2026-10-19T12:00:00Z'});const copy=validateWorkspace(JSON.parse(JSON.stringify(value)),project);assert.equal(copy.manuscripts[0].text,'첫 줄\n둘째 줄');assert.equal(metrics(project,copy).chaptersWithDraft,1);assert.equal(project.manuscripts.length,3);assert.equal(project.manuscripts[0].text,readFileSync(new URL('../manuscripts/000-prologue.md',import.meta.url),'utf8').replace(/\r\n/g,'\n').trimEnd());});
test('scanner returns candidates even for negation and never a contradiction verdict',()=>{const found=scanExpressions('에드는 연금술을 쓸 수 없었다\n진리와 이슈발라는 같은가');assert.equal(found.length,2);assert.equal(found[1].line,2);assert.ok(found.every(r=>!('verdict' in r)));});
test('scanner has no false success when no expressions match',()=>assert.deepEqual(scanExpressions('아침에 길을 걸었다'),[]));
test('unknown chapter and invalid timestamps do not import',()=>{const value=blankWorkspace();value.manuscripts.push({chapter:'ch99',text:'원고',savedAt:'x'});assert.throws(()=>validateWorkspace(value,project));});

test('published manuscript text matches source files and hashes',()=>{
 for(const m of project.manuscripts){const source=readFileSync(new URL('../manuscripts/'+m.file,import.meta.url),'utf8').replace(/\r\n/g,'\n').replace(/\n+$/,'');assert.equal(m.text,source);assert.equal(m.characters,source.length);assert.equal(m.sha256,createHash('sha256').update(source).digest('hex'));assert.equal(m.status,'DRAFT');}
});
test('submitted prose stays intact except the documented spelling correction',()=>{const [p,c]=project.manuscripts;assert.ok(p.text.startsWith('프롤로그 — 연금술을 못 쓰는 연금술사\n\n“거기 아니야.”'));assert.ok(c.text.includes('오랜만에 돌아온 리셈블은 별로 변하지 않았다.'));assert.ok(c.text.endsWith('기차는 동쪽으로 달렸다.'));assert.ok(c.text.includes('“네 글자야.”'));});

test('approved revision chain changes only logged passages and preserves every older version',()=>{
 for(const order of [1,2]){
  const current=project.manuscripts.find(m=>m.order===order);
  const changes=project.proofreading.corrections.filter(c=>c.manuscript===current.id);
  let expected=readFileSync(new URL('../'+changes[0].originalFile,import.meta.url),'utf8').replace(/\r\n/g,'\n').trimEnd();
  for(const c of changes){const saved=readFileSync(new URL('../'+c.originalFile,import.meta.url),'utf8').replace(/\r\n/g,'\n').trimEnd();assert.equal(saved,expected);assert.equal(expected.split(c.before).length,2);expected=expected.replace(c.before,c.after);}
  assert.equal(current.text,expected);assert.equal(current.version,order===1?5:4);
 }
 const episode=project.manuscripts.find(m=>m.order===2);assert.ok(episode.text.includes('그냥 가설이야.'));assert.ok(!episode.text.includes('연단술까지 간 거야.'));assert.ok(episode.text.includes('땅은 멈추어 있지 않는다.'));
});
test('episode two is preserved and every analysis quote exists in its source',()=>{const episode=project.manuscripts.find(m=>m.order===2);assert.equal(episode.title,'신의 이름');assert.ok(episode.text.endsWith('이슈발라란 무엇인가.'));assert.ok(episode.text.includes('나는 절반이 이슈발인이지만'));for(const item of [...project.analysis.findings,...project.analysis.checks,...project.analysis.threads])for(const e of item.evidence){const m=project.manuscripts.find(m=>m.id===e.manuscript);assert.ok(m, e.manuscript);assert.ok(m.text.includes(e.quote),e.quote);}});
test('current review keeps canon checks distinct from observed clues and hypothesis',()=>{assert.equal(project.analysis.findings.length,8);assert.equal(project.analysis.checks.length,9);assert.equal(project.analysis.threads.length,8);assert.ok(project.analysis.findings.find(f=>f.id==='a01').sources.includes('miles-secondary'));assert.ok(project.analysis.findings.every(f=>f.state==='OPEN'));assert.ok(project.analysis.threads.every(t=>t.status!=='회수 완료'));});

 test('latest submitted prose matches the received body except two logged surface edits',()=>{
 for(const source of project.proofreading.submissions){const m=project.manuscripts.find(m=>m.id===source.manuscript);let raw=readFileSync(new URL('../'+source.receivedFile,import.meta.url),'utf8').replace(/\r\n/g,'\n');assert.equal(createHash('sha256').update(raw).digest('hex'),source.receivedSha256);const blocks=raw.trimEnd().split('\n\n');let expected=blocks[0]+' — '+blocks[1]+'\n\n'+blocks.slice(2).join('\n\n');for(const c of project.proofreading.corrections.filter(c=>c.manuscript===m.id))expected=expected.replace(c.before,c.after);assert.equal(m.text,expected);}
 assert.equal(project.proofreading.corrections.length,2);
 });

 test('multi-paragraph evidence resolves the complete excerpt instead of the first common phrase',()=>{const prose='제목\n\n아무것도 없었다.\n\n중간 장면.\n\n없었다.\n\n종이가 찢겨 있었다.';assert.equal(evidenceParagraph(prose,'없었다.\n\n종이가 찢겨 있었다.'),3);assert.equal(evidenceParagraph(prose,'없는 인용'),0);});
