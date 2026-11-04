import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const comics=JSON.parse(readFileSync(new URL('../site/data/comics.json',import.meta.url),'utf8'));
const chapter=n=>comics.find(c=>c.number===n);
test('comic images retain matching content-hashed responsive variants and unique originals',()=>{
 for(const ch of comics){
  assert.equal(new Set(ch.pages.map(p=>p.original)).size,ch.pages.length);
  for(const p of ch.pages){
   assert.ok(p.width>0 && p.height>0);
   assert.match(p.src,/-[a-f0-9]{12}-1080\.webp$/);
   assert.equal(p.small,p.src.replace(/-1080\.webp$/,'-720.webp'));
   assert.match(p.original,/^comics\/\d{2}\/.+\.jpg$/);
  }
 }
});
test('verified first corrections remain and debate supplements appear before meeting conclusion',()=>{
 for(const [n,name] of [[3,'03-page-02-rev1.jpg'],[5,'05-page-04-rev1.jpg'],[8,'09-page-08-rev1.jpg'],[9,'08-page-07-rev1.jpg']])
  assert.ok(chapter(n).pages.some(p=>p.original.endsWith('/'+name)));
 const seven=chapter(7).pages.map(p=>p.original.split('/').pop());
 const anchor=seven.indexOf('03-page-02.jpg');
 assert.deepEqual(seven.slice(anchor+1,anchor+4),['r2-ch07-insert-1.jpg','r2-ch07-insert-2.jpg','r2-ch07-insert-3.jpg']);
 assert.equal(seven[anchor+4],'04-page-03-rev2.jpg');
 const four=chapter(4).pages.map(p=>p.original.split('/').pop());
 assert.deepEqual(four.slice(-3),['09-page-08-rev2.jpg','r2-ch04-insert-1.jpg','r2-ch04-insert-2.jpg']);
});
