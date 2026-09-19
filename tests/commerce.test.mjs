import {test,after} from 'node:test';
import assert from 'node:assert/strict';
import {writeFile,mkdir,readFile} from 'node:fs/promises';
import {createHash,createHmac} from 'node:crypto';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {Miniflare}=createRequire(require.resolve('wrangler/package.json'))('miniflare');
const {build}=createRequire(require.resolve('wrangler/package.json'))('esbuild');
await mkdir('.sites-runtime/tests',{recursive:true});
const mf=new Miniflare({modules:true,script:'export default {fetch(){return new Response("ok")}}',compatibilityDate:'2026-05-15',d1Databases:['DB'],r2Buckets:['PAID_FILES']});
globalThis.__storeEnv={DB:await mf.getD1Database('DB'),PAID_FILES:await mf.getR2Bucket('PAID_FILES'),STRIPE_SECRET_KEY:'sk_test_fixture_not_a_secret',STRIPE_WEBHOOK_SECRET:'whsec_test_fixture'};
const STRIPE_WEBHOOK_SECRET='whsec_test_fixture';
await build({entryPoints:['server/commerce.ts'],bundle:true,define:{'import.meta.env.VITE_STORE_PREVIEW':'"false"'},format:'esm',platform:'node',outfile:'.sites-runtime/tests/commerce.mjs',plugins:[{name:'isolated-bindings',setup(b){b.onResolve({filter:/^cloudflare:workers$/},()=>({path:'env',namespace:'fixture'}));b.onResolve({filter:/api\/_shared$/},()=>({path:'auth',namespace:'fixture'}));b.onLoad({filter:/.*/,namespace:'fixture'},a=>({contents:a.path==='env'?'export const env=globalThis.__storeEnv;':`export const isStoreOwner=u=>u?.userId==='owner';export async function signedIn(r){const id=r.headers.get('authorization');return id?{userId:id,email:id==='owner'?'ksaintpierre@lexcs.org':'buyer@example.test'}:null;}`,loader:'js'}))}}]});
const s=await import('../.sites-runtime/tests/commerce.mjs');
await s.initialize();
const releaseBeforeProvision=await s.publicCatalog();
assert.equal(releaseBeforeProvision.filter(p=>p.ready).length,162);
await s.provision();
const D=globalThis.__storeEnv.DB;
const id='aaaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa';
let remote,remoteSub,creates=0;
function parseForm(raw){return Object.fromEntries(new URLSearchParams(raw).entries())}
function lineItems(form){const items=[];for(let i=0;;i++){const name=form[`line_items[${i}][price_data][product_data][name]`];if(name===undefined)break;items.push({name,unit_amount:Number(form[`line_items[${i}][price_data][unit_amount]`]),quantity:Number(form[`line_items[${i}][quantity]`])})}return items}
function payNow(){remote.payment_status='paid';remote.payment_intent={id:'pi_test_123456789',status:'succeeded',amount:remote.amount_total,currency:'usd'}}
const realFetch=globalThis.fetch;
globalThis.fetch=async(url,opts={})=>{const u=String(url),method=opts.method||'GET';
 if(method==='POST'&&u==='https://api.stripe.com/v1/checkout/sessions'){creates++;const form=parseForm(opts.body);
  if(form['mode']==='subscription'){remoteSub={id:'sub_test_123456789',status:'active',current_period_end:Math.floor(Date.now()/1000)+2592000};remote={id:'cs_test_sub_123456789',url:'https://checkout.stripe.com/c/pay/cs_test_sub_123456789',mode:'subscription',subscription:remoteSub.id,metadata:{user_id:form['metadata[user_id]'],plan:form['metadata[plan]']}};return Response.json(remote)}
  const items=lineItems(form);remote={id:'cs_test_123456789',url:'https://checkout.stripe.com/c/pay/cs_test_123456789',client_reference_id:form['client_reference_id'],currency:'usd',amount_total:items.reduce((sum,it)=>sum+it.unit_amount*it.quantity,0),payment_status:'unpaid',payment_intent:null,line_items:items};return Response.json(remote)}
 if(method==='GET'&&u.startsWith('https://api.stripe.com/v1/checkout/sessions/'))return Response.json(remote);
 if(method==='GET'&&u.startsWith('https://api.stripe.com/v1/subscriptions/'))return Response.json(remoteSub);
 throw new Error('Unexpected outbound request: '+method+' '+u)};
function req(action,input,who='owner'){return new Request('https://store.example/api/store/'+action,{method:input===undefined?'GET':'POST',headers:{...(who?{authorization:who}:{}),'Content-Type':'application/json'},...(input===undefined?{}:{body:JSON.stringify(input)})})}
after(async()=>{globalThis.fetch=realFetch;await mf.dispose()});
test('rejects unauthenticated purchase and owner sales',async()=>{assert.equal((await s.safe(()=>s.createOrder(req('create',{},'')))).status,401);assert.equal((await s.safe(()=>s.sales(req('sales',undefined,'stranger')))).status,403)});
test('existing catalog PDFs retain their exact bytes after storage compaction',async()=>{
 const payload=JSON.parse(await readFile('server/legacy-resource-payload.json','utf8'));
 for(const [id,file] of Object.entries(payload.files)){
  const stored=await globalThis.__storeEnv.PAID_FILES.get('products/2026-09-15-researched/'+id+'.pdf');
  assert.ok(stored);
  const bytes=Buffer.from(await stored.arrayBuffer());
  assert.equal(bytes.length,file.bytes);
  assert.equal(createHash('sha256').update(bytes).digest('hex'),file.sha256);
 }
});
test('server ignores forged browser prices and rejects unknown products',async()=>{const bad=await s.safe(()=>s.createOrder(req('create',{productIds:['made-up'],requestKey:crypto.randomUUID(),total:1})));assert.equal(bad.status,409);const result=await s.createOrder(req('create',{productIds:['ca-grade4-multidigit'],requestKey:id,total:1,price:1,name:'fraud',downloadPath:'/etc/passwd'}));assert.equal(result.status,200);assert.equal(remote.amount_total,500);assert.equal(remote.line_items[0].name,'Multi-Digit Operations: Place-Value Strategies');const again=await s.createOrder(req('create',{productIds:['ca-grade4-multidigit'],requestKey:id}));assert.equal(again.status,200);assert.equal(creates,1)});
test('cancel/unapproved state provides no download',async()=>{assert.equal((await s.safe(()=>s.downloadToken(req('download-token',{productId:'ca-grade4-multidigit'})))).status,403)});
test('successful payment and duplicate confirmation fulfill once',async()=>{payNow();await s.confirmOrder(req('confirm',{sessionId:remote.id}));await s.confirmOrder(req('confirm',{sessionId:remote.id}));const row=await D.prepare('SELECT * FROM store_orders').first();assert.equal(row.status,'completed');assert.equal(row.fulfillment,'available')});
test('wrong account cannot get or redeem a download',async()=>{assert.equal((await s.safe(()=>s.downloadToken(req('download-token',{productId:'ca-grade4-multidigit'},'stranger')))).status,403);const {token}=await (await s.downloadToken(req('download-token',{productId:'ca-grade4-multidigit'}))).json();assert.equal((await s.safe(()=>s.download(req('download',{token},'stranger')))).status,403);const response=await s.download(req('download',{token}));assert.equal(response.headers.get('Content-Type'),'application/pdf');assert.equal(new TextDecoder().decode((await response.arrayBuffer()).slice(0,4)),'%PDF');assert.equal((await s.safe(()=>s.download(req('download',{token})))).status,403)});
test('expired download is denied',async()=>{const {token}=await(await s.downloadToken(req('download-token',{productId:'ca-grade4-multidigit'}))).json();await D.prepare('UPDATE store_download_tokens SET expires_at=0 WHERE token_hash=?').bind(await s.digest(token)).run();assert.equal((await s.safe(()=>s.download(req('download',{token})))).status,403)});
function event(type,id,object,{badSig=false}={}){const payload=JSON.stringify({id,type,created:Math.floor(Date.now()/1000),data:{object}});const timestamp=Math.floor(Date.now()/1000);const sig=badSig?'0'.repeat(64):createHmac('sha256',STRIPE_WEBHOOK_SECRET).update(timestamp+'.'+payload).digest('hex');return new Request('https://store.example/api/store/webhook',{method:'POST',headers:{'stripe-signature':`t=${timestamp},v1=${sig}`},body:payload})}
test('bad signature is rejected, duplicate webhook is recorded once',async()=>{const object={id:remote.id,client_reference_id:remote.client_reference_id};assert.equal((await s.safe(()=>s.webhook(event('checkout.session.completed','bad',object,{badSig:true})))).status,400);await s.webhook(event('checkout.session.completed','complete1',object));await s.webhook(event('checkout.session.completed','complete1',object));assert.equal((await D.prepare("SELECT COUNT(*) n FROM store_webhooks WHERE id='complete1'").first()).n,1)});
test('refund revokes access and late completed event cannot restore it',async()=>{const {token}=await(await s.downloadToken(req('download-token',{productId:'ca-grade4-multidigit'}))).json();await s.webhook(event('charge.refunded','refund1',{id:'ch_refund_test',payment_intent:'pi_test_123456789',currency:'usd',amount_refunded:500}));assert.equal((await s.safe(()=>s.download(req('download',{token})))).status,403);await s.webhook(event('checkout.session.completed','complete2',{id:remote.id,client_reference_id:remote.client_reference_id}));assert.equal((await D.prepare('SELECT status FROM store_orders').first()).status,'refunded')});
test('anonymous configuration never exposes a sandbox checkout',async()=>{const response=await s.configuration(req('configuration',undefined,''));assert.equal(response.status,200);const c=await response.json();assert.equal(c.enabled,false);assert.equal(c.liveOpen,false);assert.equal(c.mode,null)});
test('customers cannot use owner-only sandbox checkout',async()=>{assert.equal((await s.safe(()=>s.createOrder(req('create',{productIds:['fl-grade5-theme'],requestKey:crypto.randomUUID()},'customer')))).status,403)});
test('private drafts cannot be fetched or bought even with a known identifier',async()=>{await D.prepare('UPDATE store_products SET approved=0 WHERE id=?').bind('fl-grade5-theme').run();assert.equal((await s.publicCatalog()).some(p=>p.id==='fl-grade5-theme'),false);assert.equal((await s.safe(()=>s.createOrder(req('create',{productIds:['fl-grade5-theme'],requestKey:crypto.randomUUID()})))).status,409)});
test('unprepared products cannot be bought',async()=>{await D.prepare('UPDATE store_products SET ready=0 WHERE id=?').bind('tx-grade7-elements-compounds').run();assert.equal((await s.safe(()=>s.createOrder(req('create',{productIds:['tx-grade7-elements-compounds'],requestKey:crypto.randomUUID()})))).status,409)});
test('live checkout stays closed unless explicitly enabled',async()=>{const testKey=globalThis.__storeEnv.STRIPE_SECRET_KEY;globalThis.__storeEnv.STRIPE_SECRET_KEY='sk_live_test_fixture';try{assert.equal((await s.safe(()=>s.createOrder(req('create',{productIds:['college-algebra-linear'],requestKey:crypto.randomUUID()})))).status,503);assert.equal((await(await s.configuration(req('configuration',undefined))).json()).enabled,false)}finally{globalThis.__storeEnv.STRIPE_SECRET_KEY=testKey}});
test('invalid amounts, foreign origins and malformed JSON fail safely',async()=>{assert.throws(()=>s.mutation(new Request('https://store.example/api/store/create',{headers:{origin:'https://attacker.example'}})));const malformed=new Request('https://store.example/api/store/create',{method:'POST',headers:{authorization:'owner'},body:'{broken'});assert.equal((await s.safe(()=>s.createOrder(malformed))).status,400)});
test('new full resource files require the owner or a paid entitlement',async()=>{
 const productId='nc-g3-equal-groups-teaching-bundle';
 assert.equal((await s.publicCatalog()).find(p=>p.id===productId).ready,true);
 assert.equal((await s.safe(()=>s.ownerResourceFile(req('owner-file',{productId,format:'pdf'},'')))).status,401);
 assert.equal((await s.safe(()=>s.ownerResourceFile(req('owner-file',{productId,format:'pdf'},'customer')))).status,403);
 assert.equal((await s.safe(()=>s.downloadToken(req('download-token',{productId},'customer')))).status,403);
 const manifest=JSON.parse(await readFile('data/resource-release-manifest.json','utf8'));
 for(const format of ['pdf','pptx','slides','default']){
  const response=await s.ownerResourceFile(req('owner-file',{productId,format}));
  const name=manifest.products[productId][format],expected=manifest.files[name];
  assert.equal(response.headers.get('Content-Type'),expected.contentType);
  assert.equal(response.headers.get('Cache-Control'),'private, no-store');
  assert.equal(createHash('sha256').update(Buffer.from(await response.arrayBuffer())).digest('hex'),expected.sha256);
 }
 assert.equal((await s.safe(()=>s.ownerResourceFile(req('owner-file',{productId:'../../etc/passwd',format:'pdf'})))).status,404);
});
test('a paid bundle download returns its exact ZIP and refund revokes it',async()=>{
 const productId='nc-g3-equal-groups-teaching-bundle',orderId='fixture-bundle-paid';
 await D.prepare("INSERT INTO store_orders(id,user_id,email,mode,request_key,total_cents,status,fulfillment) VALUES(?,?,?,?,?,?,?,?)").bind(orderId,'bundle-buyer','buyer@example.test','sandbox','fixture-bundle',1200,'completed','available').run();
 await D.prepare('INSERT INTO store_order_items(order_id,product_id,title,amount_cents) VALUES(?,?,?,?)').bind(orderId,productId,'Fixture bundle',1200).run();
 const {token}=await(await s.downloadToken(req('download-token',{productId},'bundle-buyer'))).json();
 const response=await s.download(req('download',{token},'bundle-buyer'));
 const manifest=JSON.parse(await readFile('data/resource-release-manifest.json','utf8'));
 assert.equal(response.headers.get('Content-Type'),'application/zip');
 assert.equal(createHash('sha256').update(Buffer.from(await response.arrayBuffer())).digest('hex'),manifest.files[productId+'.zip'].sha256);
 await D.prepare("UPDATE store_orders SET status='refunded',fulfillment='revoked' WHERE id=?").bind(orderId).run();
 assert.equal((await s.safe(()=>s.downloadToken(req('download-token',{productId},'bundle-buyer')))).status,403);
});

test('resource updates replace old private pointers and repair unprepared files',async()=>{const product='college-programming-python';await D.prepare('UPDATE store_products SET storage_key=?,ready=1 WHERE id=?').bind('products/old-python.pdf',product).run();await s.provision();let row=await D.prepare('SELECT storage_key,ready FROM store_products WHERE id=?').bind(product).first();assert.match(row.storage_key,/2026-09-15-researched/);assert.equal(row.ready,1);assert.ok(await globalThis.__storeEnv.PAID_FILES.head(row.storage_key));await D.prepare('UPDATE store_products SET ready=0 WHERE id=?').bind(product).run();await s.provision();row=await D.prepare('SELECT ready FROM store_products WHERE id=?').bind(product).first();assert.equal(row.ready,1)});
test('approved daily releases are listed while full files still require owner or paid access',async()=>{
 const drafts=JSON.parse(await readFile('server/daily-drafts-2026-09-15.json','utf8'));
 const visible=new Set((await s.publicCatalog()).map(p=>p.id));
 const before=creates;
 for(const p of drafts){
  assert.ok(visible.has(p.id));
  const row=await D.prepare('SELECT approved,ready FROM store_products WHERE id=?').bind(p.id).first();assert.equal(row.approved,1);assert.equal(row.ready,1);
  for(const who of ['', 'customer'])assert.equal((await s.safe(()=>s.ownerResourceFile(req('owner-file',{productId:p.id,format:'pdf'},who)))).status,who?403:401);
  assert.equal((await s.safe(()=>s.downloadToken(req('download-token',{productId:p.id},'customer')))).status,403);
  for(const format of ['pdf','thumbnail']){
   const response=await s.ownerResourceFile(req('owner-file',{productId:p.id,format}));assert.equal(response.status,200);assert.equal(response.headers.get('Cache-Control'),'private, no-store');
   const expected=await readFile('resources/private-drafts/2026-09-15/'+p.id+(format==='pdf'?'.pdf':'-thumbnail.png'));
   assert.ok(Buffer.from(await response.arrayBuffer()).equals(expected));
  }
 }
 assert.equal(creates,before,'Unpaid download attempts must never reach Stripe');
});


test('the complete release supports protected delivery for every new product',async()=>{
 const release=JSON.parse(await readFile('data/sales-release-2026-09-15.json','utf8'));
 const payload=JSON.parse(await readFile('server/resource-payload.json','utf8'));
 assert.equal(release.length,162);
 for(const p of release){
  const row=await D.prepare('SELECT approved,ready,storage_key FROM store_products WHERE id=?').bind(p.id).first();
  assert.equal(row.approved,1,p.id);assert.equal(row.ready,1,p.id);assert.match(row.storage_key,/^bundled\//);
  const orderId='release-fixture-'+p.id;
  await D.prepare('INSERT INTO store_orders(id,user_id,email,mode,request_key,total_cents,status,fulfillment) VALUES(?,?,?,?,?,?,?,?)').bind(orderId,'release-buyer','buyer@example.test','sandbox',orderId,p.priceCents,'completed','available').run();
  await D.prepare('INSERT INTO store_order_items(order_id,product_id,title,amount_cents) VALUES(?,?,?,?)').bind(orderId,p.id,p.title,p.priceCents).run();
  const {token}=await(await s.downloadToken(req('download-token',{productId:p.id},'release-buyer'))).json();
  const response=await s.download(req('download',{token},'release-buyer'));
  const name=payload.products[p.id].default,expected=payload.files[name];
  assert.equal(response.status,200,p.id);assert.equal(response.headers.get('Content-Type'),expected.contentType);
  assert.equal(createHash('sha256').update(Buffer.from(await response.arrayBuffer())).digest('hex'),expected.sha256,p.id);
  await D.prepare("UPDATE store_orders SET status='refunded',fulfillment='revoked' WHERE id=?").bind(orderId).run();
  assert.equal((await s.safe(()=>s.downloadToken(req('download-token',{productId:p.id},'release-buyer')))).status,403,p.id);
 }
});
test('released product can be withdrawn without anonymous catalog initialization reapproving it',async()=>{
 const id='daily-20260915-ma-pk-rhyme-circle';
 await D.prepare('UPDATE store_products SET approved=0 WHERE id=?').bind(id).run();
 assert.equal((await s.publicCatalog()).some(p=>p.id===id),false);
 assert.equal((await s.safe(()=>s.createOrder(req('create',{productIds:[id],requestKey:crypto.randomUUID()})))).status,409);
 await s.provision();assert.equal((await s.publicCatalog()).find(p=>p.id===id).ready,true);
});
test('verified original slide packages require owner upload and paid delivery',async()=>{
 const specs=JSON.parse(await readFile('server/ela-upload-manifest.json','utf8'));
 for(const [id,spec] of Object.entries(specs)){
  const bytes=await readFile('resources/ela-release/'+spec.name);
  const upload=(who,data=bytes,origin='https://store.example')=>new Request('https://store.example/api/store/owner-upload?productId='+id,{method:'POST',headers:{authorization:who,origin,'content-type':'application/zip'},body:data});
  assert.equal((await s.publicCatalog()).some(p=>p.id===id),false);
  assert.equal((await s.safe(()=>s.uploadOwnerFile(upload('customer')))).status,403);
  assert.equal((await s.safe(()=>s.uploadOwnerFile(upload('owner',bytes,'https://attacker.example')))).status,403);
  assert.equal((await s.safe(()=>s.uploadOwnerFile(upload('owner',Buffer.from('wrong file'))))).status,422);
  assert.equal((await s.safe(()=>s.uploadOwnerFile(upload('owner',Buffer.alloc(spec.bytes+1))))).status,413);
  const result=await (await s.uploadOwnerFile(upload('owner'))).json();assert.equal(result.sha256,spec.sha256);
  assert.equal((await s.publicCatalog()).find(p=>p.id===id).ready,true);
  const own=await s.ownerResourceFile(req('owner-file',{productId:id,format:'default'}));assert.equal(createHash('sha256').update(Buffer.from(await own.arrayBuffer())).digest('hex'),spec.sha256);
  assert.equal((await s.safe(()=>s.downloadToken(req('download-token',{productId:id},'customer')))).status,403);
  const oid=crypto.randomUUID();await D.prepare("INSERT INTO store_orders(id,user_id,email,mode,request_key,total_cents,status,fulfillment) VALUES(?,?,?,?,?,?,'completed','available')").bind(oid,'customer','customer@example.com','sandbox',crypto.randomUUID(),800).run();
  await D.prepare('INSERT INTO store_order_items(order_id,product_id,title,amount_cents) VALUES(?,?,?,?)').bind(oid,id,id,800).run();
  const {token}=await(await s.downloadToken(req('download-token',{productId:id},'customer'))).json();const file=await s.download(req('download',{token},'customer'));assert.equal(file.headers.get('Content-Type'),'application/zip');assert.equal(createHash('sha256').update(Buffer.from(await file.arrayBuffer())).digest('hex'),spec.sha256);
  await D.prepare("UPDATE store_orders SET status='refunded',fulfillment='revoked' WHERE id=?").bind(oid).run();assert.equal((await s.safe(()=>s.downloadToken(req('download-token',{productId:id},'customer')))).status,403);
 }
});
test('subscribing requires a real plan, and the webhook activates access',async()=>{
 assert.equal((await s.safe(()=>s.createSubscriptionCheckout(req('subscribe',{plan:'made-up-plan'})))).status,400);
 const result=await s.createSubscriptionCheckout(req('subscribe',{plan:'generator-monthly'}));
 assert.equal(result.status,200);
 const {checkoutUrl}=await result.json();
 assert.equal(checkoutUrl,'https://checkout.stripe.com/c/pay/cs_test_sub_123456789');
 assert.equal(remote.mode,'subscription');
 assert.equal(await s.activeSubscription('owner','generator-monthly'),null,'checkout alone must not grant access before the webhook confirms it');
 await s.webhook(event('checkout.session.completed','sub-complete1',remote));
 const active=await s.activeSubscription('owner','generator-monthly');
 assert.ok(active);
 assert.equal(active.status,'active');
 assert.equal((await s.safe(()=>s.createSubscriptionCheckout(req('subscribe',{plan:'generator-monthly'})))).status,409,'an already-active subscriber cannot start a second checkout for the same plan');
});
test('a lapsed payment revokes access, and cancellation is reflected in subscription status',async()=>{
 await s.webhook(event('customer.subscription.updated','sub-update1',{id:remoteSub.id,status:'past_due',current_period_end:remoteSub.current_period_end}));
 assert.equal(await s.activeSubscription('owner','generator-monthly'),null,'past_due must not count as active');
 await s.webhook(event('customer.subscription.updated','sub-update2',{id:remoteSub.id,status:'active',current_period_end:remoteSub.current_period_end}));
 assert.ok(await s.activeSubscription('owner','generator-monthly'),'access is restored once billing succeeds again');
 await s.webhook(event('customer.subscription.deleted','sub-delete1',{id:remoteSub.id,status:'canceled',current_period_end:remoteSub.current_period_end}));
 assert.equal(await s.activeSubscription('owner','generator-monthly'),null);
 const status=await(await s.subscriptionStatus(req('subscription-status',undefined))).json();
 assert.equal(status.subscriptions[0].status,'canceled');
});
