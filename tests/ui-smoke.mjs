import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const author = JSON.parse(await readFile(new URL('../author-site/data/project.json', import.meta.url), 'utf8'));

async function render(search) {
  const elements = new Map();
  globalThis.document = {
    querySelector(selector) {
      if (!elements.has(selector)) elements.set(selector, { innerHTML: '', textContent: '', href: '' });
      return elements.get(selector);
    },
    querySelectorAll() { return []; },
  };
  globalThis.location = { search, pathname: '/east/admin/', hostname: 'localhost', protocol: 'http:' };
  globalThis.history = { replaceState() {} };
  globalThis.fetch = async () => ({ ok: true, json: async () => author });
  globalThis.scrollTo = () => {};
  await import(`${new URL('../site/app.js', import.meta.url).href}?smoke=${encodeURIComponent(search)}`);
  return elements.get('#main').innerHTML;
}

test('admin review shows all chapters, four status checks and exact length', async () => {
  const html = await render('?view=analysis&review=23');
  assert.match(html, /전체 화 결과/);
    assert.match(html, /<th>캐릭터<\/th><th>개연성<\/th><th>스토리라인<\/th><th>세계관·복선<\/th>/);
    assert.doesNotMatch(html, /<th>분량<\/th>|<th>종합<\/th>/);
  assert.match(html, /5,070자/);
  assert.doesNotMatch(html, /\/ 10|\/10/);
});

test('storyline tabs render chapter plans, setting canon notes, and green paid seeds', async () => {
  const chapters = await render('?view=storyline&tab=chapters');
  assert.match(chapters, /제13화/);
  assert.match(chapters, /서쪽에서 온 사람/);
  assert.match(chapters, /story-review/);
  assert.match(chapters, /발자취/);
  assert.match(chapters, /반영한 수정/);
  const settings = await render('?view=storyline&tab=settings');
  assert.match(settings, /본편 대비 개연성/);
  assert.match(settings, /카이룬/);
  assert.match(settings, /옛 안족 영역/);
  const foreshadowing = await render('?view=storyline&tab=foreshadowing');
  assert.match(foreshadowing, /회수 성공/);
  assert.match(foreshadowing, /paid-off/);
});
