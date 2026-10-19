import { chapterLabel, normalizeChapterIndex, normalizeView } from './core.mjs';

const $ = selector => document.querySelector(selector);
const esc = value => String(value ?? '').replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));

let project;
const params = new URLSearchParams(location.search);
let view = normalizeView(params.get('view'));
let chapterIndex = 0;
let reviewIndex = 0;

function isAuthor() { return project.audience === 'author'; }

function updateUrl() {
  const next = new URLSearchParams();
  next.set('view', view);
  if (view === 'analysis') next.set('review', String(reviewIndex));
  if (view === 'read' && chapterIndex > 0) next.set('chapter', String(chapterIndex));
  history.replaceState(null, '', `${location.pathname}?${next}`);
}

function adminUrl() {
  if (['127.0.0.1', 'localhost'].includes(location.hostname)) return 'http://127.0.0.1:8092/?view=read';
  return `${location.protocol}//${location.hostname}:10000/east/admin/?view=read`;
}

function publicUrl() {
  if (['127.0.0.1', 'localhost'].includes(location.hostname)) return 'http://127.0.0.1:8091/?view=read';
  return `${location.protocol}//${location.hostname}:10000/east/?view=read`;
}

function homeUrl() {
  if (['127.0.0.1', 'localhost'].includes(location.hostname)) return 'http://127.0.0.1:8087/';
  return `${location.protocol}//${location.hostname}:10000/`;
}

function inline(text) {
  return esc(text)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.+?)`/g, '<code>$1</code>');
}

function prose(text) {
  return text.split(/\n\s*\n/).map(paragraph => {
    const trimmed = paragraph.trim();
    if (['⸻', '*', '-', '---'].includes(trimmed)) return '<div class="scene-break" aria-label="장면 전환">⸻</div>';
    if (trimmed.startsWith('> ')) return `<blockquote>${inline(trimmed.replace(/^>\s?/gm, ''))}</blockquote>`;
    return `<p>${inline(paragraph)}</p>`;
  }).join('');
}

function emptyReader() {
  return `<section class="empty-state"><span class="empty-mark">原</span><h1>새 원고를 기다리고 있어</h1><p>확정한 스토리라인에 맞춰 프롤로그부터 다시 등록할 예정이야.<br>원고가 들어오면 이 화면에서 회차별로 읽을 수 있어.</p>${isAuthor() ? '<span class="admin-note">관리자 모드 · 이전 원고는 아래 보관함에서만 확인 가능</span>' : ''}</section>`;
}

function historyView() {
  if (!isAuthor() || !project.history?.length) return '';
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

function charactersPage() {
  const characters = project.publicCharacters || [];
  const groups = characters.reduce((all, item) => {
    const key = item.group || '기타';
    (all[key] ||= []).push(item);
    return all;
  }, {});
  return `<header class="characters-head"><span>CHARACTERS</span><h1>이야기를 함께 걷는 사람들</h1><p>소속별로 나누고, 지금 이야기에서 어떤 인물과 연결되는지도 적었어.</p></header>${Object.entries(groups).map(([group, people]) => `<section class="character-group"><header><span>FACTION</span><h2>${esc(group)}</h2><p>${esc(people[0].groupDescription || '')}</p></header><div class="character-grid">${people.map(item => `<article class="character-card"><span>${esc(item.affiliation || group)}</span><h2>${esc(item.name)}</h2><p>${esc(item.summary)}</p><dl><dt>연관성</dt><dd>${esc(item.relationship || '이야기의 흐름과 연결되는 인물.')}</dd></dl></article>`).join('')}</div></section>`).join('')}`;
}

function reviewPage() {
  const reviews = project.chapterReviews || [];
  if (!reviews.length) return `<section class="empty-state"><h1>아직 검토할 원고가 없어</h1><p>원고를 등록하면 이곳에서 회차별 검토를 남길 수 있어.</p></section>`;
  reviewIndex = normalizeChapterIndex(reviewIndex, reviews.length);
  const review = reviews[reviewIndex];
  return `<header class="analysis-head"><span>AUTHOR REVIEW</span><h1>원고를 읽고<br>근거를 남긴다</h1><p>점수는 현재 원고가 확정 스토리라인과 검증 규칙을 얼마나 지키는지 보는 편집 메모야. 작품의 정답을 자동으로 만들지는 않아.</p></header><nav class="review-index" aria-label="원고 검토 선택">${reviews.map((item, index) => `<button data-review="${index}" class="${reviewIndex === index ? 'active' : ''}" ${reviewIndex === index ? 'aria-current="page"' : ''}>${esc(item.episode)}<small>${esc(item.title)}</small></button>`).join('')}</nav><section class="review-hero"><div><span>OVERALL</span><h2>${esc(review.episode)} · ${esc(review.title)}</h2><p>${esc(review.summary)}</p></div><strong>${Number(review.score).toFixed(1)}<small>/ 10</small></strong></section><section class="review-grid">${review.categories.map(item => `<article class="review-card"><header><span>${esc(item.name)}</span><b>${Number(item.score).toFixed(1)}<small>/10</small></b></header><p>${esc(item.assessment)}</p><dl><dt>원고에서 확인한 근거</dt><dd>${esc(item.evidence)}</dd></dl></article>`).join('')}</section><aside class="next-checks"><span>NEXT CHECK</span><h2>다음 원고에서 확인할 것</h2><ul>${review.nextChecks.map(item => `<li>${esc(item)}</li>`).join('')}</ul></aside><aside class="method-note">검토 기준: 캐릭터가 원작의 중심을 지키는지, 사건의 원인과 정보 전달이 연결되는지, 세계관이 새 힘으로 덮이지 않는지, 심은 질문이 다음 장면으로 자연스럽게 이어지는지를 함께 본다.</aside>`;
}

function render() {
  $('#navigation').innerHTML = `<button data-view="read" class="${view === 'read' ? 'active' : ''}"><span>01</span>글 읽기</button><button data-view="characters" class="${view === 'characters' ? 'active' : ''}"><span>02</span>등장인물</button>${isAuthor() ? `<button data-view="analysis" class="${view === 'analysis' ? 'active' : ''}"><span>03</span>글 분석</button>` : ''}`;
  $('#mode-link').href = isAuthor() ? publicUrl() : adminUrl();
  $('#home-brand').href = homeUrl();
  $('#home-link').href = homeUrl();
  $('#mode-link').textContent = isAuthor() ? '공개 화면으로' : '관리자 모드';
  $('#mode-badge').textContent = isAuthor() ? 'AUTHOR' : 'READER';
  $('#breadcrumb').textContent = view === 'read' ? '글 읽기' : view === 'characters' ? '등장인물' : '글 분석 / 회차별 검토';
  $('#main').innerHTML = view === 'read' ? readPage() : view === 'characters' ? charactersPage() : reviewPage();
  document.querySelectorAll('[data-view]').forEach(button => button.onclick = () => {
    view = button.dataset.view; updateUrl(); render(); scrollTo({top: 0});
  });
  document.querySelectorAll('[data-chapter]').forEach(button => button.onclick = () => {
    chapterIndex = Number(button.dataset.chapter); view = 'read'; updateUrl(); render(); scrollTo({top: 0, behavior: 'smooth'});
  });
  document.querySelectorAll('[data-scroll-top]').forEach(button => button.onclick = () => {
    scrollTo({top: 0, behavior: 'smooth'});
  });
  document.querySelectorAll('[data-review]').forEach(button => button.onclick = () => {
    reviewIndex = Number(button.dataset.review); view = 'analysis'; updateUrl(); render(); scrollTo({top: 0, behavior: 'smooth'});
  });
}

try {
  const response = await fetch('./data/project.json');
  if (!response.ok) throw new Error('프로젝트 자료를 불러오지 못했습니다.');
  project = await response.json();
  chapterIndex = normalizeChapterIndex(params.get('chapter'), project.manuscripts?.length ?? 0);
  reviewIndex = normalizeChapterIndex(params.get('review'), project.chapterReviews?.length ?? 0);
  if (!isAuthor() && view === 'analysis') view = 'read';
  updateUrl();
  render();
} catch (error) {
  $('#main').innerHTML = `<section class="empty-state"><h1>기록을 불러오지 못했어</h1><p>${esc(error.message)}</p></section>`;
}
