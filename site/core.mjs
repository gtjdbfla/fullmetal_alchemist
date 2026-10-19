export const VIEWS = ['read', 'analysis'];

export const ANALYSIS_SECTIONS = ['characters', 'causality', 'world'];

export function normalizeView(value) {
  return VIEWS.includes(value) ? value : 'read';
}

export function normalizeAnalysisSection(value) {
  return ANALYSIS_SECTIONS.includes(value) ? value : 'characters';
}

export function chapterLabel(chapter, index) {
  if (chapter.episode) return chapter.episode;
  return index === 0 ? '프롤로그' : `${index}화`;
}
