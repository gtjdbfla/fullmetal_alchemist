import test from 'node:test';
import assert from 'node:assert/strict';

test('comic reader loads without manuscript data and fetches other views only when selected', async () => {
  const elements = new Map();
  let navigation = [];
  const requests = [];
  globalThis.document = {
    querySelector(selector) {
      if (!elements.has(selector)) elements.set(selector, {});
      return elements.get(selector);
    },
    querySelectorAll(selector) {
      if (selector === '[data-view]') {
        navigation = ['comic', 'read'].map(view => ({dataset: {view}}));
        return navigation;
      }
      return [];
    },
  };
  globalThis.location = {search: '?view=comic', pathname: '/east/', hostname: 'localhost', protocol: 'http:'};
  globalThis.history = {replaceState() {}};
  globalThis.scrollTo = () => {};
  globalThis.fetch = async path => {
    requests.push(path);
    return {ok: true, json: async () => path.includes('comics') ? [{episode: '프롤로그', title: '프롤로그', pages: [{src: 'large.webp', small: 'small.webp', original: 'original.jpg', label: '표지', width: 1080, height: 1350}]}] : {manuscripts: []}};
  };
  await import('../site/app.js');
  assert.deepEqual(requests, ['./data/comics.json']);
  assert.match(elements.get('#main').innerHTML, /srcset="small.webp 720w, large.webp 1080w"/);
  assert.match(elements.get('#main').innerHTML, /fetchpriority="high"/);
  assert.match(elements.get('#main').innerHTML, /href="original.jpg"/);
  navigation.find(button => button.dataset.view === 'read').onclick();
  await new Promise(resolve => setImmediate(resolve));
  assert.deepEqual(requests, ['./data/comics.json', './data/project.json']);
  navigation.find(button => button.dataset.view === 'comic').onclick();
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(requests.length, 2);
  assert.match(elements.get('#main').innerHTML, /large.webp/);
});
