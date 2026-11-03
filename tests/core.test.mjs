import test from 'node:test';
import assert from 'node:assert/strict';
import { chapterLabel, normalizeAnalysisSection, normalizeChapterIndex, normalizeView, NAVIGATION, renderNavigation } from '../site/core.mjs';

test('navigation accepts reader, character, and administrator workspace views', () => {
  assert.equal(normalizeView('read'), 'read');
  assert.equal(normalizeView('comic'), 'comic');
  assert.equal(normalizeView('characters'), 'characters');
  assert.equal(normalizeView('analysis'), 'analysis');
  assert.equal(normalizeView('storyline'), 'storyline');
  assert.equal(normalizeView('world'), 'read');
});

test('analysis only exposes the three requested sections', () => {
  assert.equal(normalizeAnalysisSection('characters'), 'characters');
  assert.equal(normalizeAnalysisSection('causality'), 'causality');
  assert.equal(normalizeAnalysisSection('world'), 'world');
  assert.equal(normalizeAnalysisSection('politics'), 'characters');
});

test('chapter labels keep the prologue and numbered flow readable', () => {
  assert.equal(chapterLabel({}, 0), '프롤로그');
  assert.equal(chapterLabel({}, 2), '2화');
  assert.equal(chapterLabel({episode: '제1화'}, 1), '제1화');
});

test('reader falls back to the prologue for invalid chapter choices', () => {
  assert.equal(normalizeChapterIndex('0', 3), 0);
  assert.equal(normalizeChapterIndex('2', 3), 2);
  assert.equal(normalizeChapterIndex('-1', 3), 0);
  assert.equal(normalizeChapterIndex('3', 3), 0);
  assert.equal(normalizeChapterIndex('not-a-number', 3), 0);
});


test('all dashboard tabs share one link style and exactly one current state', () => {
  assert.deepEqual(NAVIGATION.map(item => item.view), ['comic', 'read', 'characters', 'analysis', 'storyline']);
  for (const item of NAVIGATION) {
    const html = renderNavigation(item.view);
    assert.equal((html.match(/class="nav-item/g) || []).length, 5);
    assert.equal((html.match(/aria-current="page"/g) || []).length, 1);
    assert.match(html, new RegExp(`href="${item.href.replace(/[?]/g, '\\?')}" class="nav-item active"`));
  }
});
