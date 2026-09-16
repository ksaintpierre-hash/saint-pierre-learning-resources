import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile,access} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const catalog=JSON.parse(await readFile('data/catalog-expansion-2026-09-15.json','utf8'));
const manifest=JSON.parse(await readFile('data/resource-release-manifest.json','utf8'));
test('every empty collection has thirty distinct complete bundle listings',()=>{
 assert.equal(catalog.length,90);assert.equal(new Set(catalog.map(p=>p.id)).size,90);
 for(const name of Object.keys(manifest.stats.collectionCounts))assert.equal(new Set(catalog.filter(p=>p.collections.includes(name)).map(p=>p.id)).size,30,name);
 for(const p of catalog){
  for(const field of ['title','description','detailedDescription','included','grades','state','subject','resourceType','formats','pages','minutes','studentDirections','teacherUse','answerKey','accessibility','preparation','digitalNotes','license','originality','priceCents','tags','thumbnailAlt','publicationStatus'])assert.ok(p[field],p.id+': '+field);
  assert.equal(p.approved,true);
  if(p.audience==='Educators and families')assert.equal(p.state,'State-neutral');
 }
});
test('all public previews and thumbnails exist, while full files stay server-only',async()=>{
 for(const p of catalog){await access('public/product-thumbnails/'+p.id+'.png');for(const preview of p.previews)await access('public'+preview.src);}
 for(const name of Object.keys(manifest.files)){await assert.rejects(access('public/'+name));await assert.rejects(access('public/resources/'+name));}
});
test('all 180 private files reconstruct to their verified SHA-256 without altered bytes',async()=>{
 const payload=JSON.parse(await readFile('server/resource-payload.json','utf8'));const chunks=payload.chunks.map(s=>Buffer.from(s,'base64'));
 assert.equal(Object.keys(manifest.files).length,180);
 for(const name of Object.keys(manifest.files)){
  const file=payload.files[name];assert.ok(file,name);
  const bytes=Buffer.concat(file.chunks.map(i=>chunks[i]));assert.equal(bytes.length,file.bytes,name);
  assert.equal(createHash('sha256').update(bytes).digest('hex'),manifest.files[name].sha256,name);
 }
});
