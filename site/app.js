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

function storyBiblePanels() {
  const bible = project.storyBible;
  if (!bible) return `<aside class="method-note">Story Bible 구조 데이터를 준비 중이야.</aside>`;
  const chapterRows = bible.chapters.map(item => `<tr class="${esc(item.status).toLowerCase()}"><td>${esc(item.label)}</td><td><b>${esc(item.title)}</b></td><td>${esc(item.status)}</td><td>${esc(item.characterCount)}</td><td>${esc(item.mainQuestion)}</td><td>${esc(item.mainEvent)}</td><td>${esc(item.pov)}</td><td>${esc(item.edwardRole)}</td><td><span class="continuity ${esc(item.continuity).toLowerCase()}">${esc(item.continuity)}</span></td></tr>`).join('');
  return `<section class="bible-dashboard">
    <div class="section-title bible-title"><div><span>STORY BIBLE v${esc(bible.version)}</span><h2>집필과 검증을 위한 구조 데이터</h2></div><p>${esc(bible.purpose)}</p></div>
    <section class="bible-panel"><header><span>CHAPTER TIMELINE</span><h3>회차별 역할</h3></header><div class="timeline-scroll"><table class="chapter-timeline"><thead><tr><th>회차</th><th>제목</th><th>상태</th><th>글자 수</th><th>중심 질문</th><th>핵심 사건</th><th>시점</th><th>에드 역할</th><th>정합성</th></tr></thead><tbody>${chapterRows}</tbody></table></div></section>
    <section class="bible-panel"><header><span>CHARACTER ARC TRACKER</span><h3>인물 아크</h3></header><div class="arc-grid">${bible.characterArcs.map(item => `<article class="arc-card"><h4>${esc(item.name)}</h4><dl><dt>현재 심리 단계</dt><dd>${esc(item.current)}</dd><dt>목표</dt><dd>${esc(item.goal)}</dd><dt>갈등</dt><dd>${esc(item.conflict)}</dd><dt>다음 필수 비트</dt><dd>${esc(item.nextBeat)}</dd></dl></article>`).join('')}</div></section>
    <section class="bible-panel"><header><span>FORESHADOWING TRACKER</span><h3>복선의 심기와 회수</h3></header><div class="foreshadow-grid">${bible.foreshadowing.map(item => `<article class="foreshadow-card"><header><span>${esc(item.status)}</span><h4>${esc(item.plot)}</h4></header><dl><dt>심기</dt><dd>${esc(item.planted)}</dd><dt>강화</dt><dd>${esc(item.reinforcement)}</dd><dt>회수</dt><dd>${esc(item.payoff)}</dd><dt>위험</dt><dd>${esc(item.risk)}</dd></dl></article>`).join('')}</div></section>
    <section class="bible-panel"><header><span>KNOWLEDGE STATE TRACKER</span><h3>인물별 정보 상태</h3></header><div class="knowledge-grid">${bible.knowledgeStates.map(item => `<article class="knowledge-card"><h4>${esc(item.name)}</h4><dl><dt>아는 것</dt><dd>${esc(item.knows)}</dd><dt>모르는 것</dt><dd>${esc(item.unknown)}</dd><dt>다음 확인</dt><dd>${esc(item.next)}</dd></dl></article>`).join('')}</div></section>
    <section class="bible-panel"><header><span>CAUSAL CHAIN VIEW</span><h3>인과 체인</h3></header><div class="chain-stack">${bible.causalChains.map(chain => `<article class="chain-card"><h4>${esc(chain.title)}</h4><ol>${chain.steps.map(step => `<li>${esc(step)}</li>`).join('')}</ol></article>`).join('')}</div></section>
    <section class="bible-panel"><header><span>HARD RULE MONITOR</span><h3>고정 규칙</h3></header><div class="rule-grid">${bible.hardRules.map(item => `<article class="rule-card ${esc(item.level).toLowerCase()}"><header><span>${esc(item.level)}</span><b>${esc(item.status)}</b></header><h4>${esc(item.rule)}</h4><p>${esc(item.description)}</p><small>${esc(item.note)}</small></article>`).join('')}</div></section>
    <section class="bible-panel change-panel"><header><span>CHANGE IMPACT ANALYSIS</span><h3>설정 변경 전 확인</h3></header><ol>${bible.changeImpact.map(item => `<li>${esc(item)}</li>`).join('')}</ol><p>승인 원고와 Story Bible이 충돌하면 어느 한쪽을 자동으로 고치지 않고, 사용자 결정이 필요한 충돌로 기록한다.</p></section>
    <aside class="method-note">원고 검토 순서: ${bible.reviewProtocol.map(item => esc(item)).join(' → ')}. 설정 변경의 우선순위: ${bible.sourcePolicy.map(item => esc(item)).join(' → ')}.</aside>
  </section>`;
}

function storylinePage() {
  const story = project.storyline;
  if (!story) return `<section class="empty-state"><h1>스토리라인을 준비 중이야</h1><p>활성 스토리라인 문서를 정리하면 이곳에 표시돼.</p></section>`;
  const alignment = story.alignment;
  return `<header class="analysis-head"><span>STORYLINE MASTER</span><h1>${esc(story.title)}</h1><p>${esc(story.summary)}</p></header><section class="story-progress"><div><span>MANUSCRIPT PROGRESS</span><h2>${story.currentChapter}화 <small>/ ${story.totalChapters}화</small></h2><div class="progress-track"><i style="width:${Number(story.progress)}%"></i></div><p>현재 원고는 ${esc(story.currentRange)}까지 작성됨 · 전체 진행률 ${Number(story.progress).toFixed(1)}%</p></div><div class="alignment-score"><span>STORYLINE FIT</span><strong>${Number(alignment.score).toFixed(1)}<small>/10</small></strong><p>${esc(alignment.label)}</p></div></section><section class="metric-grid">${alignment.metrics.map(item => `<article><span>${esc(item.name)}</span><b>${esc(item.value)}</b><p>${esc(item.note)}</p></article>`).join('')}</section><section class="story-themes"><span>CORE QUESTIONS</span><h2>이야기가 향하는 질문</h2><ul>${story.coreQuestions.map(item => `<li>${esc(item)}</li>`).join('')}</ul></section><section class="part-board"><div class="section-title"><div><span>STORY MAP</span><h2>전체 진행 지도</h2></div><p>완료된 원고와 앞으로의 계획을 분리해 본다.</p></div>${story.parts.map(part => `<article class="part-card ${part.status.toLowerCase()}"><header><div><span>${esc(part.label)} · ${esc(part.episodes)}</span><h3>${esc(part.title)}</h3></div><b>${esc(part.statusLabel)}</b></header><p>${esc(part.summary)}</p><dl><dt>개연성의 핵심</dt><dd>${esc(part.causality)}</dd><dt>떡밥·회수</dt><dd>${esc(part.foreshadowing)}</dd><dt>설정 경계</dt><dd>${esc(part.worldRule)}</dd></dl></article>`).join('')}</section><section class="mystery-board"><div class="section-title"><div><span>ACTIVE THREADS</span><h2>현재 떡밥과 설정 상태</h2></div><p>가설과 작품의 실제 설정을 같은 사실로 취급하지 않는다.</p></div>${story.threads.map(item => `<article class="mystery-card"><header><span>${esc(item.status)}</span><h3>${esc(item.title)}</h3></header><dl><dt>현재 원고</dt><dd>${esc(item.current)}</dd><dt>향후 진행</dt><dd>${esc(item.next)}</dd><dt>주의할 점</dt><dd>${esc(item.guardrail)}</dd></dl></article>`).join('')}</section>${storyBiblePanels()}<aside class="method-note">정합 점수는 현재 승인 원고의 회차별 검토와 Story Bible의 하드 룰을 함께 반영한다. 점수가 높다고 해서 앞으로의 전개를 자동으로 확정하는 것은 아니다.</aside>`;
}

function render() {
  $('#navigation').innerHTML = `<button data-view="read" class="${view === 'read' ? 'active' : ''}"><span>01</span>글 읽기</button><button data-view="characters" class="${view === 'characters' ? 'active' : ''}"><span>02</span>등장인물</button>${isAuthor() ? `<button data-view="analysis" class="${view === 'analysis' ? 'active' : ''}"><span>03</span>글 분석</button><button data-view="storyline" class="${view === 'storyline' ? 'active' : ''}"><span>04</span>스토리라인</button>` : ''}`;
  $('#mode-link').href = isAuthor() ? publicUrl() : adminUrl();
  $('#home-brand').href = homeUrl();
  $('#home-link').href = homeUrl();
  $('#mode-link').textContent = isAuthor() ? '공개 화면으로' : '관리자 모드';
  $('#mode-badge').textContent = isAuthor() ? 'AUTHOR' : 'READER';
  $('#breadcrumb').textContent = view === 'read' ? '글 읽기' : view === 'characters' ? '등장인물' : view === 'analysis' ? '글 분석 / 회차별 검토' : '스토리라인 / 전체 진행';
  $('#main').innerHTML = view === 'read' ? readPage() : view === 'characters' ? charactersPage() : view === 'analysis' ? reviewPage() : storylinePage();
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
  if (!isAuthor() && ['analysis', 'storyline'].includes(view)) view = 'read';
  updateUrl();
  render();
} catch (error) {
  $('#main').innerHTML = `<section class="empty-state"><h1>기록을 불러오지 못했어</h1><p>${esc(error.message)}</p></section>`;
}
