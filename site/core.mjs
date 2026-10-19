export const VIEWS = ['read', 'characters', 'analysis'];

export const ANALYSIS_SECTIONS = ['characters', 'causality', 'world'];

export function normalizeView(value) {
  return VIEWS.includes(value) ? value : 'read';
}

export function normalizeAnalysisSection(value) {
  return ANALYSIS_SECTIONS.includes(value) ? value : 'characters';
}

export function normalizeChapterIndex(value, count) {
  const index = Number.parseInt(value, 10);
  return Number.isInteger(index) && index >= 0 && index < count ? index : 0;
}

export function chapterLabel(chapter, index) {
  if (chapter.episode) return chapter.episode;
  return index === 0 ? '프롤로그' : `${index}화`;
}
