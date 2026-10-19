import { ANALYSIS_SECTIONS, chapterLabel, normalizeAnalysisSection, normalizeChapterIndex, normalizeView } from './core.mjs';

const $ = selector => document.querySelector(selector);
const esc = value => String(value ?? '').replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));

let project;
const params = new URLSearchParams(location.search);
let view = normalizeView(params.get('view'));
let section = normalizeAnalysisSection(params.get('section'));
let chapterIndex = 0;

function updateUrl() {
  const next = new URLSearchParams();
  next.set('view', view);
  if (view === 'analysis') next.set('section', section);
  if (view === 'read' && chapterIndex > 0) next.set('chapter', String(chapterIndex));
  history.replaceState(null, '', `${location.pathname}?${next}`);
}

function adminUrl() {
  if (['127.0.0.1', 'localhost'].includes(location.hostname)) return 'http://127.0.0.1:8092/?view=read';
  return `${location.protocol}//${location.hostname}:8444/?view=read`;
}

function publicUrl() {
  if (['127.0.0.1', 'localhost'].includes(location.hostname)) return 'http://127.0.0.1:8091/?view=read';
  return `${location.protocol}//${location.hostname}:10000/east/?view=read`;
}

function homeUrl() {
  if (['127.0.0.1', 'localhost'].includes(location.hostname)) return 'http://127.0.0.1:8087/';
  return `${location.protocol}//${location.hostname}:10000/`;
}

function prose(text) {
  return text.split(/\n\s*\n/).map(paragraph => ['⸻', '*'].includes(paragraph.trim())
    ? '<div class="scene-break" aria-label="장면 전환">⸻</div>'
    : `<p>${esc(paragraph)}</p>`).join('');
}

function emptyReader() {
  return `<section class="empty-state"><span class="empty-mark">原</span><h1>새 원고를 기다리고 있어</h1><p>확정한 스토리라인에 맞춰 프롤로그부터 다시 등록할 예정이야.<br>원고가 들어오면 이 화면에서 회차별로 읽을 수 있어.</p>${project.audience === 'author' ? '<span class="admin-note">관리자 모드 · 이전 원고는 아래 보관함에서만 확인 가능</span>' : ''}</section>`;
}

function historyView() {
  if (project.audience !== 'author' || !project.history?.length) return '';
  return `<section class="history"><div class="section-title"><div><span>ADMIN ONLY</span><h2>이전 원고 보관함</h2></div><p>공개 화면과 현재 원고 목록에는 포함되지 않아.</p></div>${project.history.map(item => `<details><summary><b>${esc(item.episode)} · ${esc(item.title)}</b><span>v${item.version} · ${esc(item.archivedReason)}</span></summary><article class="archive-copy"><pre>${esc(item.text)}</pre></article></details>`).join('')}</section>`;
}

function readPage() {
  const chapters = project.manuscripts || [];
  if (!chapters.length) return emptyReader() + historyView();
  chapterIndex = normalizeChapterIndex(chapterIndex, chapters.length);
  const chapter = chapters[chapterIndex];
  const previous = chapterIndex - 1;
  const next = chapterIndex + 1;
  return `<section class="reader-intro"><span>MANUSCRIPT</span><h1>${esc(project.title)}</h1><p>목차에서 원하는 회차를 골라 읽어.</p><nav class="chapter-index" aria-label="회차 목차">${chapters.map((item, index) => `<button data-chapter="${index}" class="${chapterIndex === index ? 'active' : ''}" ${chapterIndex === index ? 'aria-current="page"' : ''}>${esc(chapterLabel(item, index))}</button>`).join('')}</nav></section><article class="chapter-reader"><section class="chapter" id="chapter-${chapterIndex}"><header><span>${esc(chapterLabel(chapter, chapterIndex))}</span><h2>${esc(chapter.title)}</h2></header><div class="reader-body">${prose(chapter.text)}</div></section><nav class="chapter-controls" aria-label="원고 이동"><button data-chapter="${previous}" ${previous < 0 ? 'disabled' : ''}>← 이전화</button><button data-scroll-top="true">맨 위로 · 목차</button><button data-chapter="${next}" ${next >= chapters.length ? 'disabled' : ''}>다음화 →</button></nav></article>${historyView()}`;
}

function characterView(data) {
  return `<div class="analysis-grid">${data.items.map(item => `<article class="analysis-card"><span class="card-type">CHARACTER</span><h2>${esc(item.name)}</h2><dl><dt>원작의 중심</dt><dd>${esc(item.core)}</dd><dt>이번 이야기의 변화</dt><dd>${esc(item.arc)}</dd><dt>넘지 않을 선</dt><dd>${esc(item.guardrail)}</dd></dl></article>`).join('')}</div>`;
}

function causalityView(data) {
  const mysteryBoard = data.mysteries?.length ? `<section class="mystery-board"><div class="section-title"><div><span>MYSTERY BOARD</span><h2>가설과 실제 상태를 분리한다</h2></div><p>작품의 실제 상태는 에드의 인식과 다를 수 있어.</p></div>${data.mysteries.map(item => `<article class="mystery-card"><h3>${esc(item.question)}</h3><dl><dt>에드의 현재 가설</dt><dd>${esc(item.hypothesis)}</dd><dt>반대 증거</dt><dd>${esc(item.counterEvidence)}</dd><dt>작품의 실제 상태</dt><dd>${esc(item.actualState)}</dd></dl></article>`).join('')}</section>` : '';
  return `<section class="causal-flow">${data.chain.map((step, index) => `<div><small>${String(index + 1).padStart(2, '0')}</small><b>${esc(step)}</b></div>`).join('')}</section>${mysteryBoard}<div class="analysis-grid compact">${data.checks.map(item => `<article class="analysis-card"><span class="card-type">CHECK</span><h2>${esc(item.name)}</h2><p>${esc(item.test)}</p></article>`).join('')}</div><section class="score-line"><span>장별 24점 검토</span>${data.score.map(item => `<b>${esc(item)}</b>`).join('')}</section>`;
}

function worldView(data) {
  return `<div class="classification">${data.classes.map(item => `<article><b>${esc(item.name)}</b><p>${esc(item.meaning)}</p></article>`).join('')}</div><div class="analysis-split"><section class="analysis-card"><span class="card-type">POWER GUARDRAILS</span><h2>세계의 힘을 키우지 않는다</h2><ul>${data.guardrails.map(item => `<li>${esc(item)}</li>`).join('')}</ul></section><section class="analysis-card"><span class="card-type">LEDGERS</span><h2>세계의 변화를 기록한다</h2><div class="ledger-list">${data.ledgers.map(item => `<span>${esc(item)}</span>`).join('')}</div></section></div>`;
}

function analysisPage() {
  const current = project.analysis[section];
  const body = section === 'characters' ? characterView(current) : section === 'causality' ? causalityView(current) : worldView(current);
  return `<header class="analysis-head"><span>STORY REVIEW</span><h1>이야기가 커져도<br>무너지지 않게</h1><p>${esc(current.description)}</p></header><nav class="subtabs" aria-label="분석 분류">${ANALYSIS_SECTIONS.map(key => `<button data-section="${key}" class="${section === key ? 'active' : ''}">${esc(project.analysis[key].title)}</button>`).join('')}</nav>${body}<aside class="method-note">새 원고가 등록되면 이 규칙을 기준으로 장면의 근거와 감점 이유를 연결해. 가설은 사실로 자동 승격하지 않고, 점수보다 왜 걸렸는지를 남겨.</aside>`;
}

function render() {
  $('#navigation').innerHTML = `<button data-view="read" class="${view === 'read' ? 'active' : ''}"><span>01</span>글 읽기</button><button data-view="analysis" class="${view === 'analysis' ? 'active' : ''}"><span>02</span>글 분석</button>`;
  $('#mode-link').href = project.audience === 'author' ? publicUrl() : adminUrl();
  $('#home-brand').href = homeUrl();
  $('#home-link').href = homeUrl();
  $('#mode-link').textContent = project.audience === 'author' ? '공개 화면으로' : '관리자 모드';
  $('#mode-badge').textContent = project.audience === 'author' ? 'AUTHOR' : 'READER';
  $('#breadcrumb').textContent = view === 'read' ? '글 읽기' : `글 분석 / ${project.analysis[section].title}`;
  $('#main').innerHTML = view === 'read' ? readPage() : analysisPage();
  document.querySelectorAll('[data-view]').forEach(button => button.onclick = () => {
    view = button.dataset.view; updateUrl(); render(); scrollTo({top: 0});
  });
  document.querySelectorAll('[data-chapter]').forEach(button => button.onclick = () => {
    chapterIndex = Number(button.dataset.chapter); view = 'read'; updateUrl(); render(); scrollTo({top: 0, behavior: 'smooth'});
  });
  document.querySelectorAll('[data-scroll-top]').forEach(button => button.onclick = () => {
    scrollTo({top: 0, behavior: 'smooth'});
  });
  document.querySelectorAll('[data-section]').forEach(button => button.onclick = () => {
    section = button.dataset.section; updateUrl(); render(); scrollTo({top: 0});
  });
}

try {
  const response = await fetch('./data/project.json');
  if (!response.ok) throw new Error('프로젝트 자료를 불러오지 못했습니다.');
  project = await response.json();
  chapterIndex = normalizeChapterIndex(params.get('chapter'), project.manuscripts?.length ?? 0);
  render();
} catch (error) {
  $('#main').innerHTML = `<section class="empty-state"><h1>기록을 불러오지 못했어</h1><p>${esc(error.message)}</p></section>`;
}
