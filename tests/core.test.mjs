import test from 'node:test';
import assert from 'node:assert/strict';
import { chapterLabel, normalizeAnalysisSection, normalizeView } from '../site/core.mjs';

test('public navigation only accepts read and analysis', () => {
  assert.equal(normalizeView('read'), 'read');
  assert.equal(normalizeView('analysis'), 'analysis');
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
