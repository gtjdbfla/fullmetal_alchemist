import { chapterLabel, normalizeChapterIndex, normalizeView } from './core.mjs';

const $ = selector => document.querySelector(selector);
const esc = value => String(value ?? '').replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));

let project;
const params = new URLSearchParams(location.search);
let view = normalizeView(params.get('view'));
let chapterIndex = 0;
let reviewIndex = 0;
let storyTab = ["chapters", "settings", "foreshadowing"].includes(params.get("tab")) ? params.get("tab") : "chapters";
let settingGroup = 0;

function isAuthor() { return project.audience === 'author'; }

function updateUrl() {
  const next = new URLSearchParams();
  next.set('view', view);
  if (view === 'analysis') next.set('review', String(reviewIndex));
  if (view === 'storyline') next.set('tab', storyTab);
  if (view === 'storyline' && storyTab === 'settings') next.set('group', String(settingGroup));
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
    .replace(/==(.+?)==/g, '<mark class="note">$1</mark>')
    .replace(/~~(.+?)~~/g, '<del class="struck">$1</del>')
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
  return `<header class="characters-head"><span>CHARACTERS</span><h1>이야기를 함께 걷는 사람들</h1><p>소속별로 나누고, 지금 이야기에서 어떤 인물과 연결되는지도 적었어.</p></header>${Object.entries(groups).map(([group, people]) => `<section class="character-group"><header><span>FACTION</span><h2>${esc(group)}</h2><p>${esc(people[0].groupDescription || '')}</p></header><div class="character-grid">${people.map(item => `<article class="character-card"><div class="character-head">${item.portrait ? `<img class="character-photo" src="${esc(item.portrait)}" alt="${esc(item.name)} 얼굴" width="96" height="120" loading="lazy">` : '<div class="character-photo blank" role="img" aria-label="사진 없음"></div>'}<div><span>${esc(item.affiliation || group)}</span><h2>${esc(item.name)}</h2></div></div><p>${esc(item.summary)}</p>${item.age ? `<p class="character-look"><b>나이대</b>${esc(item.age)}</p>` : ''}${item.appearance ? `<p class="character-look"><b>외형</b>${esc(item.appearance)}</p>` : ''}<dl><dt>연관성</dt><dd>${esc(item.relationship || '이야기의 흐름과 연결되는 인물.')}</dd></dl></article>`).join('')}</div></section>`).join('')}`;
}

function statusBadge(status, label = status) {
  const key = status === 'X' ? 'fail' : status === 'O' || status === 'PAYOFF' ? 'pass' : status === 'UNRESOLVED_BY_DESIGN' || status === 'OPEN_BY_DESIGN' ? 'info' : 'warn';
  return `<span class="state-badge ${key}">${esc(label)}</span>`;
}

function reviewPage() {
  const reviews = project.chapterReviews || [];
  if (!reviews.length) return `<section class="empty-state"><h1>아직 검토할 원고가 없어</h1></section>`;
  reviewIndex = normalizeChapterIndex(reviewIndex, reviews.length);
  const review = reviews[reviewIndex];
  const reviewByEpisode = new Map(reviews.map(item => [item.episode, item]));
    const reviewColumns = ['캐릭터', '개연성', '스토리라인', '세계관·복선'];
    const rows = (project.manuscripts || []).map(chapter => {
    const item = reviewByEpisode.get(chapter.episode);
    const count = chapter.characters ?? chapter.text?.length ?? 0;
      const categoryCells = reviewColumns.map(name => {
        const category = item?.categories?.find(entry => entry.name === name);
        return `<td>${category ? statusBadge(category.status) : '—'}</td>`;
      }).join('');
    const reason = item ? item.summary : '회차별 검토 기록을 준비 중';
      return `<tr><td>${esc(chapter.episode)}</td><td>${esc(chapter.title)}</td><td>${count.toLocaleString()}자</td>${categoryCells}<td>${esc(reason)}</td></tr>`;
  }).join('');
  return `<header class="analysis-head"><span>AUTHOR REVIEW</span><h1>원고 검토</h1><p>O는 현재 기준과 일치, △는 확인하거나 조정할 항목, X는 수정이 필요한 충돌을 뜻한다. 글자 수 기준은 공백 포함 5,000–7,000자다.</p></header>
    <section class="review-overview"><div class="section-title"><div><span>ALL CHAPTERS</span><h2>전체 화 결과</h2></div><p>원고에 표시되는 본문을 기준으로 계수한다.</p></div><div class="timeline-scroll"><table class="chapter-timeline"><thead><tr><th>회차</th><th>제목</th><th>공백 포함</th>${reviewColumns.map(name => `<th>${esc(name)}</th>`).join('')}<th>짧은 결과</th></tr></thead><tbody>${rows}</tbody></table></div></section>
    <nav class="review-index" aria-label="원고 검토 선택">${reviews.map((item, index) => `<button data-review="${index}" class="${reviewIndex === index ? 'active' : ''}" ${reviewIndex === index ? 'aria-current="page"' : ''}>${esc(item.episode)}<small>${esc(item.title)}</small></button>`).join('')}</nav>
    <section class="review-hero"><div><span>CHAPTER REVIEW</span><h2>${esc(review.episode)} · ${esc(review.title)}</h2><p>${esc(review.summary)}</p><p class="length-note">${esc(review.length?.reason || review.overallReason || '')}</p></div></section>
    <section class="review-grid">${review.categories.map(item => `<article class="review-card"><header><span>${esc(item.name)}</span>${statusBadge(item.status)}</header><p>${esc(item.assessment)}</p></article>`).join('')}</section>
    <aside class="next-checks"><span>NEXT CHECK</span><h2>다음 원고에서 확인할 것</h2><ul>${review.nextChecks.map(item => `<li>${esc(item)}</li>`).join('')}</ul></aside>`;
}

function storyReview(review) {
  const rows = [['개연성', review.plausibility], ['스토리라인', review.storyline], ['세계관·설정', review.settings]];
  const list = (title, items) => items?.length ? `<div class="review-note"><b>${esc(title)}</b><ul>${items.map(text => `<li>${esc(text)}</li>`).join('')}</ul></div>` : '';
  return `<section class="story-review" aria-label="작가용 검토"><header><span>REVIEW · ${esc(review.reviewer)} · ${esc(review.reviewedAt)}</span></header>${rows.map(([name, item]) => `<div class="story-review-row">${statusBadge(item.status)}<div><b>${esc(name)}</b><p>${esc(item.note)}</p></div></div>`).join('')}${list('반영한 수정', review.fixes)}${list('다음 점검', review.watch)}</section>`;
}

function chapterStoryPanel() {
  const bible = project.storyBible;
  const chapters = bible?.chapters || [];
  const milestones = project.storyline?.settingsMilestones || [];
  return `<section class="section-title"><div><span>CHAPTER PLAN</span><h2>각 화의 역할</h2></div><p>승인 원고와 이후 계획의 중심 질문·사건·에드 역할을 확인한다.</p></section>
    <div class="chapter-plan-grid">${chapters.map(item => `<article class="chapter-plan-card"><header><span>${esc(item.label)} · ${esc(item.status)}</span><h3>${esc(item.title)}</h3></header><p><b>중심 질문</b> ${esc(item.mainQuestion)}</p><p><b>핵심 사건</b> ${esc(item.mainEvent)}</p><p><b>에드 역할</b> ${esc(item.edwardRole)}</p>${item.review ? storyReview(item.review) : ''}</article>`).join('')}</div>
    <section class="bible-panel"><header><span>KNOWLEDGE MILESTONES</span><h3>에드의 가설과 지식 변화</h3></header><div class="timeline-scroll"><table class="chapter-timeline"><thead><tr><th>회차</th><th>에드의 가설</th><th>확신</th><th>아는 것</th><th>모르는 것</th><th>스카 목표</th><th>호엔하임</th><th>카르사·연단술</th><th>카이룬</th><th>결정권 주제</th><th>심은 복선</th><th>회수 상태</th><th>연속성 위험</th></tr></thead><tbody>${milestones.map(m => `<tr><td>${esc(m.chapter)}</td><td>${esc(m.edwardHypothesis)}</td><td>${esc(m.confidence)}</td><td>${esc(m.known)}</td><td>${esc(m.unknown)}</td><td>${esc(m.scarGoal)}</td><td>${esc(m.hohenheim)}</td><td>${esc(m.karsa)} / ${esc(m.alkahestry)}</td><td>${esc(m.kairun)}</td><td>${esc(m.decisionTheme)}</td><td>${esc(m.seed)}</td><td>${esc(m.payoff)}</td><td>${esc(m.continuityRisk)}</td></tr>`).join('')}</tbody></table></div></section>`;
}

function settingsPanel() {
  const bible = project.storyBible;
  const groups = project.storyline?.tabs?.settings?.groups || [];
  settingGroup = normalizeChapterIndex(settingGroup, groups.length);
  const group = groups[settingGroup];
  if (!group) return '';
  return `<nav class="subtabs" aria-label="설정 분류">${groups.map((g, i) => `<button data-setting-group="${i}" class="${i === settingGroup ? 'active' : ''}">${esc(g.label)}</button>`).join('')}</nav>
    ${group.map ? `<section class="bible-panel geography-map"><header><span>REGIONAL MAP</span><h3>${esc(group.map.title)}</h3></header><p>${esc(group.map.description)}</p><figure><a href="${esc(group.map.image)}" target="_blank" rel="noopener"><img src="${esc(group.map.image)}" alt="${esc(group.map.alt)}" width="1600" height="1080" loading="lazy" decoding="async"></a><figcaption>이미지를 누르면 크게 볼 수 있어. <a href="${esc(group.map.download)}" download>확대용 SVG 받기</a></figcaption></figure><ul>${group.map.notes.map(note => `<li>${esc(note)}</li>`).join('')}</ul></section>` : ''}
    <div class="setting-grid">${group.items.map(item => `<article class="setting-card"><h3>${esc(item.title)}</h3><p>${esc(item.description)}</p><dl><dt>${esc(item.canonLabel || '본편 대비 개연성')}</dt><dd>${esc(item.canon)}</dd></dl></article>`).join('')}</div>
    ${settingGroup === 0 ? `<section class="bible-panel"><header><span>CHARACTER ARC</span><h3>인물의 현재 단계와 다음 비트</h3></header><div class="arc-grid">${bible.characterArcs.map(item => `<article class="arc-card"><h4>${esc(item.name)}</h4><dl><dt>현재</dt><dd>${esc(item.current)}</dd><dt>목표</dt><dd>${esc(item.goal)}</dd><dt>갈등</dt><dd>${esc(item.conflict)}</dd><dt>다음 비트</dt><dd>${esc(item.nextBeat)}</dd></dl></article>`).join('')}</div></section>` : ''}
    ${settingGroup === 1 ? `<section class="bible-panel"><header><span>KNOWLEDGE STATE</span><h3>아는 것과 모르는 것</h3></header><div class="knowledge-grid">${bible.knowledgeStates.map(item => `<article class="knowledge-card"><h4>${esc(item.name)}</h4><dl><dt>아는 것</dt><dd>${esc(item.knows)}</dd><dt>모르는 것</dt><dd>${esc(item.unknown)}</dd><dt>다음 확인</dt><dd>${esc(item.next)}</dd></dl></article>`).join('')}</div></section>` : ''}
    ${settingGroup === 2 ? `<section class="bible-panel"><header><span>HARD RULES</span><h3>설정 경계</h3></header><div class="rule-grid">${bible.hardRules.map(item => `<article class="rule-card ${esc(item.level).toLowerCase()}"><header><span>${esc(item.level)}</span>${statusBadge(item.status === 'PASS' ? 'O' : '△')}</header><h4>${esc(item.rule)}</h4><p>${esc(item.description)}</p><small>${esc(item.note)}</small></article>`).join('')}</div></section><section class="bible-panel"><header><span>CAUSAL CHAINS</span><h3>주요 인과 연결</h3></header><div class="chain-stack">${bible.causalChains.map(chain => `<article class="chain-card"><h4>${esc(chain.title)}</h4><ol>${chain.steps.map(step => `<li>${esc(step)}</li>`).join('')}</ol></article>`).join('')}</div></section><section class="bible-panel"><header><span>CONTINUITY SCAN</span><h3>14화 이후 충돌 점검</h3></header><div class="setting-grid">${(project.storyline?.continuityConflicts || []).map(item => `<article class="setting-card"><header>${statusBadge(item.status)} <strong>${esc(item.location)}</strong></header><p>${esc(item.issue)}</p><dl><dt>최소 수정 권고</dt><dd>${esc(item.minimalFix)}</dd></dl></article>`).join('')}</div></section>` : ''}`;
}

function foreshadowPanel() {
  const items = project.storyBible?.foreshadowing || [];
  const label = {NOT_PLANTED:'심기 전', PLANTED:'심음', REINFORCED:'강화', PARTIALLY_REVEALED:'부분 공개', PAYOFF:'회수 성공', UNRESOLVED_BY_DESIGN:'의도적 미해결', OPEN_BY_DESIGN:'의도적으로 열어 둠'};
  return `<section class="section-title"><div><span>FORESHADOWING</span><h2>복선과 떡밥의 진행</h2></div><p>계획된 회수와 실제 원고에서 완료된 회수를 구분한다.</p></section><div class="foreshadow-grid">${items.map(item => `<article class="foreshadow-card ${item.status === 'PAYOFF' ? 'paid-off' : ''}"><header>${statusBadge(item.status === 'PAYOFF' || item.status === 'UNRESOLVED_BY_DESIGN' || item.status === 'OPEN_BY_DESIGN' ? item.status : '△', label[item.status] || item.status)}<h4>${esc(item.plot)}</h4></header><dl><dt>심기</dt><dd>${esc(item.planted)}</dd><dt>강화</dt><dd>${esc(item.reinforcement)}</dd><dt>회수 / 예정</dt><dd>${esc(item.payoff)}</dd><dt>현재 단계</dt><dd>${esc(label[item.status] || item.status)}</dd><dt>주의</dt><dd>${esc(item.risk)}</dd></dl></article>`).join('')}</div>`;
}

function storylinePage() {
  const story = project.storyline;
  if (!story) return `<section class="empty-state"><h1>스토리라인을 준비 중이야</h1></section>`;
  const tabs = story.tabs || {};
  const content = storyTab === 'settings' ? settingsPanel() : storyTab === 'foreshadowing' ? foreshadowPanel() : chapterStoryPanel();
  return `<header class="analysis-head"><span>STORY BIBLE v${esc(project.storyBible?.version || '')}</span><h1>스토리라인</h1><p>${esc(story.summary)}</p></header>
    <nav class="subtabs storyline-tabs" aria-label="스토리라인 세부 탭">${Object.entries(tabs).map(([key, tab]) => `<button data-story-tab="${esc(key)}" class="${storyTab === key ? 'active' : ''}" ${storyTab === key ? 'aria-current="page"' : ''}>${esc(tab.label)}</button>`).join('')}</nav>
    <p class="tab-description">${esc(tabs[storyTab]?.description || '')}</p>${content}`;
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
  document.querySelectorAll('[data-story-tab]').forEach(button => button.onclick = () => {
    storyTab = button.dataset.storyTab; updateUrl(); render(); scrollTo({top: 0});
  });
  document.querySelectorAll('[data-setting-group]').forEach(button => button.onclick = () => {
    settingGroup = Number(button.dataset.settingGroup); updateUrl(); render();
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
  settingGroup = normalizeChapterIndex(params.get('group'), project.storyline?.tabs?.settings?.groups?.length ?? 0);
  if (!isAuthor() && ['analysis', 'storyline'].includes(view)) view = 'read';
  updateUrl();
  render();
} catch (error) {
  $('#main').innerHTML = `<section class="empty-state"><h1>기록을 불러오지 못했어</h1><p>${esc(error.message)}</p></section>`;
}
