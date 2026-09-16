import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile,access} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const drafts=JSON.parse(await readFile('server/daily-drafts-2026-09-15.json','utf8'));
const payload=JSON.parse(await readFile('server/resource-payload.json','utf8'));
const catalog=JSON.parse(await readFile('data/catalog.json','utf8'));
const expansion=JSON.parse(await readFile('data/catalog-expansion-2026-09-15.json','utf8'));
test('historical draft records stay intact after explicit release approval',()=>{
 assert.equal(drafts.length,20);assert.equal(new Set(drafts.map(p=>p.id)).size,20);
 const existing=new Set([...catalog,...expansion].map(p=>p.title));
 for(const p of drafts){
  assert.equal(p.approved,false);assert.equal(p.ready,false);assert.equal(p.status,'private_draft');assert.ok(!existing.has(p.title));
  for(const field of ['title','summary','detailedDescription','included','level','standard','objective','subject','resourceType','formats','pages','minutes','studentDirections','teacherUse','answerKey','differentiation','preparation','printing','digitalUse','license','originalContent','priceCents','tags','thumbnailAlt','publicationStatus','sources'])assert.ok(p[field],p.id+': '+field);
  assert.equal(p.slides,0);assert.equal(p.formats.join(','),'PDF');assert.ok(p.pages>=15);
  for(const key of ['AIG','504','EC','ESL'])assert.ok(p.differentiation[key]);
 }
});
test('all forty historical files reconstruct exactly; complete PDFs remain private',async()=>{
 for(const p of drafts)for(const format of ['pdf','thumbnail']){
  const name=payload.products[p.id][format],file=payload.files[name];assert.ok(file);
  const data=Buffer.concat(file.chunks.map(i=>Buffer.from(payload.chunks[i],'base64')));
  assert.equal(data.length,file.bytes);assert.equal(createHash('sha256').update(data).digest('hex'),file.sha256);
  await assert.rejects(access('public/'+name));await assert.rejects(access('public/product-thumbnails/'+name));
  assert.ok(data.equals(await readFile('resources/private-drafts/2026-09-15/'+name)));
 }
});
test('draft metadata and files are gated server-side before response',async()=>{
 const route=await readFile('app/api/owner/route.ts','utf8');
 assert.ok(route.indexOf('if(!isStoreOwner(user))')<route.indexOf('approvedResources,dailyDrafts}'));
 const commerce=await readFile('server/commerce.ts','utf8');
 const handler=commerce.slice(commerce.indexOf('export async function ownerResourceFile'));
 assert.ok(handler.indexOf('if(!owner(user))')<handler.indexOf('resourceFile(input.productId'));
 assert.match(commerce,/WHERE approved=1/);assert.match(commerce,/approved=1 AND ready=1/);
 const client=await readFile('app/components/DailyDrafts.tsx','utf8');assert.ok(!client.includes('server/daily-drafts'));
 const server=await readFile('server/resource-files.ts','utf8');assert.match(server,/Object.hasOwn\(products,id\)/);
});
test('rotation records all twenty unique titles and exact state rather than nationwide credits',async()=>{
 const tracker=JSON.parse(await readFile('data/product-tracker.json','utf8'));
 for(const p of drafts){const found=tracker.completed.filter(q=>q.id===p.id);assert.equal(found.length,1);assert.equal(found[0].standard,p.standard);}
 assert.equal(Object.keys(tracker.stateCoverageCounts).length,50);
 assert.equal(new Set(drafts.filter(p=>p.state).map(p=>p.state)).size,9);
});
