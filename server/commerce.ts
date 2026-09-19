import { PREVIEW_MODE } from '../lib/preview-mode';
import { env } from 'cloudflare:workers';
import catalog from '../data/catalog.json';
import elaRelease from '../data/ela-release.json';
import elaFiles from './ela-upload-manifest.json';
import salesRelease from '../data/sales-release-2026-09-15.json';
import catalogExpansion from '../data/catalog-expansion-2026-09-15.json';
import { privateProducts } from './private-products';
import { hasResourceFile, resourceFile, resourceMetadata } from './resource-files';
import dailyDrafts from './daily-drafts-2026-09-15.json';
import { signedIn, isStoreOwner } from '../app/api/_shared';
const releaseIds=new Set(salesRelease.map(p=>p.id));
const listingMetadata=[...catalog,...salesRelease,...elaRelease];
export const originalListing=(id:string):Record<string,unknown>|undefined=>listingMetadata.find(p=>p.id===id);
export const hasOriginalListing=(id:string)=>listingMetadata.some(p=>p.id===id);
const inventory=[...listingMetadata,...dailyDrafts.filter(p=>!releaseIds.has(p.id))];

export class StoreError extends Error { constructor(public status:number,message:string){super(message)} }
export const db = () => {if(!env.DB)throw new StoreError(503,'Store database is unavailable.');return env.DB;};
const setting=(key:string)=>Reflect.get(env,key) as string|undefined;
// Stripe test/live mode is intrinsic to the secret key itself (sk_test_/sk_live_),
// so there is no separate mode toggle to accidentally leave mismatched.
export const mode=()=>setting('STRIPE_SECRET_KEY')?.startsWith('sk_live_')?'live':'sandbox';
export const owner=(user:{userId:string}|null)=>isStoreOwner(user);
export async function customer(request:Request){const user=await signedIn(request);if(!user)throw new StoreError(401,'Please log in to your store account.');return user;}
export const json=(body:unknown,status=200)=>Response.json(body,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
export async function safe(action:()=>Promise<Response>){try{return await action()}catch(e){return json({error:e instanceof StoreError?e.message:'The store could not complete this request. Please try again or contact support.'},e instanceof StoreError?e.status:503)}}
export async function rawBody(request:Request){
 const max=131072;if(Number(request.headers.get('content-length')||0)>max)throw new StoreError(413,'Request too large.');
 const reader=request.body?.getReader();if(!reader)throw new StoreError(400,'Invalid request.');let size=0;const chunks:Uint8Array[]=[];
 while(true){const {done,value}=await reader.read();if(done)break;size+=value.length;if(size>max){await reader.cancel();throw new StoreError(413,'Request too large.')}chunks.push(value)}
 const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.length}return new TextDecoder().decode(bytes);}
export async function body(request:Request){const text=await rawBody(request);try{return JSON.parse(text)}catch{throw new StoreError(400,'Invalid request.')}}

export function mutation(request:Request){if(PREVIEW_MODE)throw new StoreError(403,'This is a read-only preview. Payments and changes are disabled.');const origin=request.headers.get('origin');if(origin&&origin!==new URL(request.url).origin)throw new StoreError(403,'Invalid request origin.');}
const schema=[
`CREATE TABLE IF NOT EXISTS store_products(id TEXT PRIMARY KEY,title TEXT NOT NULL,price_cents INTEGER NOT NULL CHECK(price_cents>0),approved INTEGER NOT NULL DEFAULT 0,metadata TEXT NOT NULL,storage_key TEXT NOT NULL,ready INTEGER NOT NULL DEFAULT 0)`,
`CREATE TABLE IF NOT EXISTS store_orders(id TEXT PRIMARY KEY,user_id TEXT NOT NULL,email TEXT NOT NULL,mode TEXT NOT NULL,request_key TEXT NOT NULL,session_id TEXT UNIQUE,payment_intent_id TEXT UNIQUE,total_cents INTEGER NOT NULL,currency TEXT NOT NULL DEFAULT 'USD',status TEXT NOT NULL DEFAULT 'created',fulfillment TEXT NOT NULL DEFAULT 'waiting',created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,paid_at TEXT,lock_until INTEGER NOT NULL DEFAULT 0,UNIQUE(user_id,mode,request_key))`,
`CREATE TABLE IF NOT EXISTS store_order_items(order_id TEXT NOT NULL,product_id TEXT NOT NULL,title TEXT NOT NULL,amount_cents INTEGER NOT NULL,PRIMARY KEY(order_id,product_id))`,
`CREATE TABLE IF NOT EXISTS store_webhooks(id TEXT PRIMARY KEY,mode TEXT NOT NULL,event_type TEXT NOT NULL,resource_id TEXT,event_time TEXT,received_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,processed INTEGER NOT NULL DEFAULT 0)`,
`CREATE TABLE IF NOT EXISTS store_download_tokens(token_hash TEXT PRIMARY KEY,user_id TEXT NOT NULL,order_id TEXT NOT NULL,product_id TEXT NOT NULL,expires_at INTEGER NOT NULL,used_at TEXT)`,
`CREATE TABLE IF NOT EXISTS store_downloads(id TEXT PRIMARY KEY,user_id TEXT NOT NULL,order_id TEXT NOT NULL,product_id TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)`,
`CREATE TABLE IF NOT EXISTS store_refunds(id TEXT PRIMARY KEY,order_id TEXT NOT NULL,amount_cents INTEGER NOT NULL,status TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)`,
`CREATE TABLE IF NOT EXISTS store_subscriptions(id TEXT PRIMARY KEY,user_id TEXT NOT NULL,mode TEXT NOT NULL,plan TEXT NOT NULL,status TEXT NOT NULL,current_period_end INTEGER,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)`,
`CREATE INDEX IF NOT EXISTS store_orders_customer ON store_orders(user_id,mode,created_at)`,
`CREATE INDEX IF NOT EXISTS store_downloads_customer ON store_downloads(user_id,created_at)`,
`CREATE INDEX IF NOT EXISTS store_subscriptions_customer ON store_subscriptions(user_id,mode)`];
export async function initialize(){
 await db().batch(schema.map(sql=>db().prepare(sql)));
 await db().batch(inventory.map(p=>db().prepare('INSERT OR IGNORE INTO store_products(id,title,price_cents,approved,metadata,storage_key,ready) VALUES(?,?,?,?,?,?,?)').bind(p.id,p.title,p.priceCents,(elaRelease.some(e=>e.id===p.id)?0:p.approved?1:0),JSON.stringify(p),'products/'+p.id+'.'+('distributionFormat' in p&&p.distributionFormat==='ZIP'?'zip':'pdf'),0)));
 await activateReleasedFiles();
}
async function activateReleasedFiles(force=false){
 // Deployment is the owner's approval of this fixed release. Migrate legacy pointers
 // once so publication does not depend on a browser login. Later withdrawals stay closed.
 const {results}=await db().prepare('SELECT id,storage_key,metadata FROM store_products').all<{id:string;storage_key:string;metadata:string}>();
 const pending=new Set(results.filter(p=>!JSON.parse(p.metadata).editorManaged&&(force||!p.storage_key.startsWith('bundled/'))).map(p=>p.id));
 // One listing with a missing file must never block every other listing's activation.
 const updates=salesRelease.filter(p=>pending.has(p.id)).flatMap(p=>{
  const file=resourceMetadata(p.id);
  if(!file||file.bytes<=0||!file.sha256)return [];
  return [db().prepare('UPDATE store_products SET title=?,price_cents=?,approved=1,metadata=?,storage_key=?,ready=1 WHERE id=?'+(force?'':" AND storage_key NOT LIKE 'bundled/%'"))
   .bind(p.title,p.priceCents,JSON.stringify(p),'bundled/'+file.sha256+'/'+file.name,p.id)];
 });
 if(updates.length)await db().batch(updates);
}
export async function provision(){
 await initialize();
 const bucket=Reflect.get(env,'PAID_FILES') as R2Bucket|undefined;
 if(!bucket)throw new StoreError(503,'Private file storage is not ready.');
 const {results}=await db().prepare('SELECT id,storage_key,ready,metadata FROM store_products WHERE approved=1').all<{id:string;storage_key:string;ready:number;metadata:string}>();
 for(const p of results){if(JSON.parse(p.metadata).editorManaged)continue;const key='products/2026-09-15-researched/'+p.id+'.pdf';if(p.ready&&p.storage_key===key)continue;const encoded=privateProducts[p.id];if(!encoded)continue;const bytes=Uint8Array.from(atob(encoded),c=>c.charCodeAt(0));await bucket.put(key,bytes,{httpMetadata:{contentType:'application/pdf'}});await db().prepare('UPDATE store_products SET ready=1,storage_key=? WHERE id=?').bind(key,p.id).run();}
 await activateReleasedFiles(true);
 return {ready:true,released:salesRelease.length};
}
export async function publicCatalog(){await initialize();const {results}=await db().prepare('SELECT id,title,price_cents,metadata,ready FROM store_products WHERE approved=1').all<{id:string;title:string;price_cents:number;metadata:string;ready:number}>();const expansionMap=Object.fromEntries(catalogExpansion.map((e:Record<string,unknown>)=>[e.id,e]));return results.map(p=>({...JSON.parse(p.metadata),...(JSON.parse(p.metadata).editorManaged?{}:listingMetadata.find(item=>item.id===p.id)),...(expansionMap[p.id]||{}),id:p.id,title:p.title,priceCents:p.price_cents,ready:!!p.ready}));}
export function configured(){return !PREVIEW_MODE && !!(setting('STRIPE_SECRET_KEY')&&setting('STRIPE_WEBHOOK_SECRET'));}
export async function checkoutAllowed(request:Request){const user=await customer(request);if(!configured())throw new StoreError(503,'Checkout is being prepared. Please check back soon.');if(mode()==='sandbox'&&!owner(user))throw new StoreError(403,'Checkout is not open yet.');if(mode()==='live'&&setting('STRIPE_LIVE_ENABLED')!=='true')throw new StoreError(503,'Checkout is not open yet.');return user;}
// Subscription plans are defined here, not accepted from the client, for the same
// reason product prices come from store_products rather than the browser's request.
export const SUBSCRIPTION_PLANS:Record<string,{name:string;priceCents:number}>={
 'generator-monthly':{name:'Practice Packet Generator — Unlimited Monthly Access',priceCents:999},
};
export async function activeSubscription(userId:string,plan:string){return db().prepare("SELECT * FROM store_subscriptions WHERE user_id=? AND mode=? AND plan=? AND status IN ('active','trialing') ORDER BY current_period_end DESC LIMIT 1").bind(userId,mode(),plan).first<{id:string;status:string;current_period_end:number|null}>();}
export async function createSubscriptionCheckout(request:Request){mutation(request);const user=await checkoutAllowed(request);await initialize();const input=await body(request);
 const plan=SUBSCRIPTION_PLANS[String(input.plan)];if(!plan)throw new StoreError(400,'Choose a plan.');
 if(await activeSubscription(user.userId,String(input.plan)))throw new StoreError(409,'You already have an active subscription to this plan.');
 const origin=new URL(request.url).origin;
 const result=await stripe('/v1/checkout/sessions','POST',{mode:'subscription',metadata:{user_id:user.userId,plan:input.plan},customer_email:user.email,success_url:origin+'/order-confirmation?session_id={CHECKOUT_SESSION_ID}',cancel_url:origin+'/cart?canceled=1',line_items:[{quantity:1,price_data:{currency:'usd',recurring:{interval:'month'},unit_amount:plan.priceCents,product_data:{name:plan.name}}}]}) as {url:string};
 return json({checkoutUrl:result.url});
}
export async function subscriptionStatus(request:Request){const user=await customer(request);await initialize();const {results}=await db().prepare('SELECT plan,status,current_period_end FROM store_subscriptions WHERE user_id=? AND mode=? ORDER BY updated_at DESC').bind(user.userId,mode()).all();return json({subscriptions:results,mode:mode()});}
// Stripe's REST API takes application/x-www-form-urlencoded bodies with bracket
// notation for nested objects/arrays (e.g. line_items[0][price_data][unit_amount]).
function formPairs(value:unknown,prefix?:string):string[]{
 if(Array.isArray(value))return value.flatMap((v,i)=>formPairs(v,prefix?`${prefix}[${i}]`:String(i)));
 if(value&&typeof value==='object')return Object.entries(value as Record<string,unknown>).flatMap(([k,v])=>formPairs(v,prefix?`${prefix}[${k}]`:k));
 if(value===undefined||value===null)return [];
 return [encodeURIComponent(prefix||'')+'='+encodeURIComponent(String(value))];
}
export async function stripe(path:string,method='GET',payload?:Record<string,unknown>,idempotencyKey?:string){
 const key=setting('STRIPE_SECRET_KEY');if(!key)throw new StoreError(503,'Stripe is not configured.');
 const qs=method==='GET'&&payload?'?'+formPairs(payload).join('&'):'';
 const response=await fetch('https://api.stripe.com'+path+qs,{method,headers:{Authorization:'Bearer '+key,...(method!=='GET'?{'Content-Type':'application/x-www-form-urlencoded'}:{}),...(idempotencyKey?{'Idempotency-Key':idempotencyKey}:{})},...(method!=='GET'&&payload?{body:formPairs(payload).join('&')}:{}),signal:AbortSignal.timeout(20000)});
 if(!response.ok)throw new StoreError(502,'Stripe could not complete this step. Check My Purchases before trying again.');
 return response.status===204?{}:await response.json();
}
export type Order={id:string;user_id:string;email:string;mode:string;session_id:string;payment_intent_id:string|null;total_cents:number;currency:string;status:string;fulfillment:string;created_at:string;paid_at:string|null};
export async function order(id:string,userId?:string){const row=await db().prepare('SELECT * FROM store_orders WHERE id=? AND mode=?'+(userId?' AND user_id=?':'')).bind(...[id,mode(),...(userId?[userId]:[])]).first<Order>();if(!row)throw new StoreError(404,'Order not found.');return row;}
export async function createOrder(request:Request){mutation(request);const user=await checkoutAllowed(request);await initialize();const input=await body(request);
 if(!Array.isArray(input.productIds)||input.productIds.length<1||input.productIds.length>20||input.productIds.some((s:unknown)=>typeof s!=='string'||s.length>100)||typeof input.requestKey!=='string'||!/^[a-f0-9-]{36}$/.test(input.requestKey))throw new StoreError(400,'Invalid cart.');
 const ids=[...new Set<string>(input.productIds)].sort();if(ids.length!==input.productIds.length)throw new StoreError(400,'Each resource needs only one teacher license.');
 const products=await Promise.all(ids.map(id=>db().prepare('SELECT id,title,price_cents,storage_key FROM store_products WHERE id=? AND approved=1 AND ready=1').bind(id).first<{id:string;title:string;price_cents:number;storage_key:string}>()));if(products.some(p=>!p))throw new StoreError(409,'A resource in your cart is not available.');
 const existing=await db().prepare('SELECT * FROM store_orders WHERE user_id=? AND mode=? AND request_key=?').bind(user.userId,mode(),input.requestKey).first<Order>();
 if(existing){const previous=await db().prepare('SELECT product_id FROM store_order_items WHERE order_id=? ORDER BY product_id').bind(existing.id).all<{product_id:string}>();if(JSON.stringify(previous.results.map(p=>p.product_id))!==JSON.stringify(ids))throw new StoreError(409,'Your cart changed. Please start a fresh checkout.');if(existing.session_id){const session=await stripe('/v1/checkout/sessions/'+existing.session_id) as {url:string};return json({checkoutUrl:session.url,localId:existing.id})}throw new StoreError(409,'This checkout is being prepared. Please wait before retrying.');}
 for(const p of products){const purchased=await db().prepare("SELECT 1 FROM store_order_items i JOIN store_orders o ON o.id=i.order_id WHERE i.product_id=? AND o.user_id=? AND o.mode=? AND o.status='completed' AND o.fulfillment='available'").bind(p!.id,user.userId,mode()).first();if(purchased)throw new StoreError(409,'You already own a resource in this cart. Open My Purchases to download it.');}
 const id=crypto.randomUUID(),total=products.reduce((sum,p)=>sum+p!.price_cents,0);
 await db().batch([db().prepare('INSERT INTO store_orders(id,user_id,email,mode,request_key,total_cents) VALUES(?,?,?,?,?,?)').bind(id,user.userId,user.email,mode(),input.requestKey,total),...products.map(p=>db().prepare('INSERT INTO store_order_items(order_id,product_id,title,amount_cents) VALUES(?,?,?,?)').bind(id,p!.id,p!.title,p!.price_cents))]);
 const origin=new URL(request.url).origin;
 const result=await stripe('/v1/checkout/sessions','POST',{mode:'payment',client_reference_id:id,metadata:{order_id:id},customer_email:user.email,success_url:origin+'/order-confirmation?session_id={CHECKOUT_SESSION_ID}',cancel_url:origin+'/cart?canceled=1',line_items:products.map(p=>({quantity:1,price_data:{currency:'usd',unit_amount:p!.price_cents,product_data:{name:p!.title}}}))},id) as {id:string;url:string};
 await db().prepare('UPDATE store_orders SET session_id=? WHERE id=?').bind(result.id,id).run();return json({checkoutUrl:result.url,localId:id});
}
export function validateSession(local:Order,remote:any){if(remote.id!==local.session_id||remote.client_reference_id!==local.id||remote.currency!=='usd'||remote.amount_total!==local.total_cents)throw new StoreError(409,'Payment verification failed. Please contact support.');const pi=remote.payment_intent;if(remote.payment_status!=='paid'||!pi||typeof pi!=='object')return null;if(pi.currency!=='usd'||pi.amount!==local.total_cents||!pi.id)throw new StoreError(409,'Payment verification failed. Please contact support.');return pi;}
export async function reconcile(local:Order,remote:any){const pi=validateSession(local,remote);if(!pi)return local;const map:Record<string,string>={succeeded:'completed',processing:'pending',canceled:'denied'};const status=map[pi.status];if(!status)return local;
 // Adverse statuses are sticky: a delayed completed event can never restore access.
 await db().prepare("UPDATE store_orders SET payment_intent_id=?,status=?,fulfillment=?,paid_at=CASE WHEN ?='completed' THEN COALESCE(paid_at,CURRENT_TIMESTAMP) ELSE paid_at END WHERE id=? AND status NOT IN ('refunded','reversed','disputed') AND (status!='completed' OR ? IN ('completed','refunded'))").bind(pi.id,status,status==='completed'?'available':status==='pending'?'waiting':'revoked',status,local.id,status).run();return order(local.id);
}
export async function confirmOrder(request:Request){mutation(request);const user=await checkoutAllowed(request);await initialize();const input=await body(request);if(typeof input.sessionId!=='string'||!/^cs_[A-Za-z0-9_]{10,80}$/.test(input.sessionId))throw new StoreError(400,'Invalid order.');const local=await db().prepare('SELECT * FROM store_orders WHERE session_id=? AND user_id=? AND mode=?').bind(input.sessionId,user.userId,mode()).first<Order>();if(!local)throw new StoreError(404,'Order not found.');if(['completed','refunded','reversed','disputed'].includes(local.status))return json(local);
 const now=Date.now();const lock=await db().prepare('UPDATE store_orders SET lock_until=? WHERE id=? AND lock_until<?').bind(now+60000,local.id,now).run();if(!lock.meta.changes)throw new StoreError(409,'Payment verification is in progress. Please check My Purchases shortly.');
 try{const remote=await stripe('/v1/checkout/sessions/'+local.session_id,'GET',{expand:['payment_intent']}) as any;if(remote.payment_status!=='paid'){if(now-Date.parse(local.created_at+'Z')>3600000)throw new StoreError(409,'This checkout expired. Please contact support before retrying.');throw new StoreError(409,'Complete your payment with Stripe first.');}return json(await reconcile(local,remote));}finally{await db().prepare('UPDATE store_orders SET lock_until=0 WHERE id=?').bind(local.id).run();}
}
// Stripe's documented webhook algorithm: HMAC-SHA256(secret, `${timestamp}.${rawBody}`),
// compared in constant time to the `v1` value, with a timestamp tolerance to block replay.
async function verifyWebhookSignature(raw:string,header:string,secret:string){
 const parts=Object.fromEntries(header.split(',').map(kv=>{const i=kv.indexOf('=');return [kv.slice(0,i),kv.slice(i+1)]}));
 const timestamp=parts['t'],sig=parts['v1'];if(!timestamp||!sig)return false;
 if(Math.abs(Date.now()/1000-Number(timestamp))>300)return false;
 const key=await crypto.subtle.importKey('raw',new TextEncoder().encode(secret),{name:'HMAC',hash:'SHA-256'},false,['sign']);
 const mac=await crypto.subtle.sign('HMAC',key,new TextEncoder().encode(timestamp+'.'+raw));
 const computed=Array.from(new Uint8Array(mac)).map(b=>b.toString(16).padStart(2,'0')).join('');
 if(computed.length!==sig.length)return false;let diff=0;for(let i=0;i<computed.length;i++)diff|=computed.charCodeAt(i)^sig.charCodeAt(i);return diff===0;
}
export async function webhook(request:Request){await initialize();if(!configured())throw new StoreError(503,'Webhook is not configured.');
 const sig=request.headers.get('stripe-signature');if(!sig)throw new StoreError(400,'Missing signature.');
 const raw=await rawBody(request);
 if(!(await verifyWebhookSignature(raw,sig,setting('STRIPE_WEBHOOK_SECRET')!)))throw new StoreError(400,'Invalid webhook signature.');
 let event:any;try{event=JSON.parse(raw)}catch{throw new StoreError(400,'Invalid event.')}
 if(!event.id||!event.type||!event.data?.object)throw new StoreError(400,'Invalid event.');
 await db().prepare('INSERT OR IGNORE INTO store_webhooks(id,mode,event_type,resource_id,event_time) VALUES(?,?,?,?,?)').bind(event.id,mode(),event.type,event.data.object.id||null,event.created?String(event.created):null).run();const receipt=await db().prepare('SELECT processed FROM store_webhooks WHERE id=?').bind(event.id).first<{processed:number}>();if(receipt?.processed)return json({received:true});
 const obj=event.data.object;
 // Subscription events are keyed by Stripe subscription id, not a store_orders row,
 // so they're handled entirely separately from the one-time-purchase flow below.
 if(event.type.startsWith('customer.subscription.')){
  await db().prepare('UPDATE store_subscriptions SET status=?,current_period_end=?,updated_at=CURRENT_TIMESTAMP WHERE id=?').bind(obj.status,obj.current_period_end?Number(obj.current_period_end):null,obj.id).run();
  await db().prepare('UPDATE store_webhooks SET processed=1 WHERE id=?').bind(event.id).run();return json({received:true});
 }
 if(event.type.startsWith('checkout.session.')&&obj.mode==='subscription'){
  if(event.type==='checkout.session.completed'&&obj.metadata?.user_id&&obj.metadata?.plan&&obj.subscription){
   const sub=await stripe('/v1/subscriptions/'+obj.subscription) as any;
   await db().prepare('INSERT INTO store_subscriptions(id,user_id,mode,plan,status,current_period_end) VALUES(?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET status=excluded.status,current_period_end=excluded.current_period_end,updated_at=CURRENT_TIMESTAMP').bind(sub.id,obj.metadata.user_id,mode(),obj.metadata.plan,sub.status,sub.current_period_end?Number(sub.current_period_end):null).run();
  }
  await db().prepare('UPDATE store_webhooks SET processed=1 WHERE id=?').bind(event.id).run();return json({received:true});
 }
 let local:Order|null=null;
 if(event.type.startsWith('checkout.session.')){
  if(obj.client_reference_id)local=await db().prepare('SELECT * FROM store_orders WHERE id=? AND mode=?').bind(obj.client_reference_id,mode()).first<Order>();
  if(!local&&obj.id)local=await db().prepare('SELECT * FROM store_orders WHERE session_id=? AND mode=?').bind(obj.id,mode()).first<Order>();
 }else if(event.type==='charge.refunded'||event.type.startsWith('charge.dispute.')){
  if(obj.payment_intent)local=await db().prepare('SELECT * FROM store_orders WHERE payment_intent_id=? AND mode=?').bind(obj.payment_intent,mode()).first<Order>();
 }
 if(local){
  if(event.type.startsWith('checkout.session.')){const session=await stripe('/v1/checkout/sessions/'+local.session_id,'GET',{expand:['payment_intent']}) as any;await reconcile(local,session);}
  else if(event.type==='charge.refunded'){if(obj.currency!=='usd')throw new StoreError(400,'Invalid currency.');await db().batch([db().prepare('INSERT OR IGNORE INTO store_refunds(id,order_id,amount_cents,status) VALUES(?,?,?,?)').bind(obj.id,local.id,obj.amount_refunded,'succeeded'),db().prepare("UPDATE store_orders SET status='refunded',fulfillment='revoked' WHERE id=?").bind(local.id)]);}
  else if(event.type.startsWith('charge.dispute.')){await db().prepare("UPDATE store_orders SET status='disputed',fulfillment='revoked' WHERE id=? AND status!='refunded'").bind(local.id).run();}
 }
 // Unknown transaction events stay unprocessed for retry; never silently lose an out-of-order refund.
 if(!local&&/^(checkout\.session\.|charge\.refunded|charge\.dispute\.)/.test(event.type))throw new StoreError(503,'Transaction is awaiting reconciliation.');
 await db().prepare('UPDATE store_webhooks SET processed=1 WHERE id=?').bind(event.id).run();return json({received:true});
}
export async function purchases(request:Request){const user=await customer(request);await initialize();const orders=await db().prepare('SELECT * FROM store_orders WHERE user_id=? AND mode=? ORDER BY created_at DESC LIMIT 100').bind(user.userId,mode()).all<Order>();const items=await db().prepare('SELECT i.* FROM store_order_items i JOIN store_orders o ON i.order_id=o.id WHERE o.user_id=? AND o.mode=?').bind(user.userId,mode()).all();const downloads=await db().prepare('SELECT product_id,created_at FROM store_downloads WHERE user_id=? ORDER BY created_at DESC LIMIT 100').bind(user.userId).all();return json({orders:orders.results,items:items.results,downloads:downloads.results,mode:mode()});}
export async function digest(s:string){return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)))).map(v=>v.toString(16).padStart(2,'0')).join('')}
export async function downloadToken(request:Request){mutation(request);const user=await customer(request);await initialize();const input=await body(request);const eligible=await db().prepare("SELECT o.id FROM store_orders o JOIN store_order_items i ON i.order_id=o.id WHERE o.user_id=? AND i.product_id=? AND o.mode=? AND o.status='completed' AND o.fulfillment='available' LIMIT 1").bind(user.userId,String(input.productId),mode()).first<{id:string}>();if(!eligible)throw new StoreError(403,'This account does not have access to that resource.');const token=crypto.randomUUID()+crypto.randomUUID();await db().prepare('INSERT INTO store_download_tokens(token_hash,user_id,order_id,product_id,expires_at) VALUES(?,?,?,?,?)').bind(await digest(token),user.userId,eligible.id,String(input.productId),Date.now()+120000).run();return json({token,expiresIn:120});}
export async function download(request:Request){mutation(request);const user=await customer(request);await initialize();const input=await body(request);if(typeof input.token!=='string'||input.token.length>100)throw new StoreError(400,'Invalid download link.');const hash=await digest(input.token);const row=await db().prepare("SELECT t.*,p.storage_key FROM store_download_tokens t JOIN store_orders o ON o.id=t.order_id JOIN store_products p ON p.id=t.product_id WHERE t.token_hash=? AND t.user_id=? AND t.expires_at>? AND t.used_at IS NULL AND o.mode=? AND o.status='completed' AND o.fulfillment='available'").bind(hash,user.userId,Date.now(),mode()).first<{product_id:string;order_id:string;storage_key:string}>();if(!row)throw new StoreError(403,'This download link expired or is no longer available. Request a new link in My Purchases.');const bucket=Reflect.get(env,'PAID_FILES') as R2Bucket|undefined;const stored=row.storage_key.startsWith('bundled/')?null:await bucket?.get(row.storage_key);const bundled=stored?null:resourceFile(row.product_id);const file=stored||bundled;if(!file)throw new StoreError(503,'Your file is temporarily unavailable. Contact support.');const used=await db().prepare('UPDATE store_download_tokens SET used_at=CURRENT_TIMESTAMP WHERE token_hash=? AND used_at IS NULL AND expires_at>?').bind(hash,Date.now()).run();if(!used.meta.changes)throw new StoreError(403,'Please request a new download link.');await db().prepare('INSERT INTO store_downloads(id,user_id,order_id,product_id) VALUES(?,?,?,?)').bind(crypto.randomUUID(),user.userId,row.order_id,row.product_id).run();return new Response(file.body,{headers:{'Content-Type':bundled?.contentType||stored?.httpMetadata?.contentType||(row.storage_key.endsWith('.zip')?'application/zip':'application/pdf'),'Content-Disposition':`attachment; filename="${bundled?.name||row.product_id+(row.storage_key.endsWith('.pptx')?'.pptx':row.storage_key.endsWith('.zip')?'.zip':'.pdf')}"`,'Cache-Control':'private, no-store','X-Content-Type-Options':'nosniff'}});}
export async function configuration(request:Request){const user=await signedIn(request);const liveOpen=configured()&&mode()==='live'&&setting('STRIPE_LIVE_ENABLED')==='true';const enabled=!!user&&configured()&&(mode()==='sandbox'?owner(user):liveOpen);return json({enabled,liveOpen,signedIn:!!user,mode:owner(user)?mode():liveOpen?'live':null});}
export async function sales(request:Request){const user=await customer(request);if(!owner(user))throw new StoreError(403,'Owner access required.');await initialize();const summary=await db().prepare(`SELECT COUNT(*) purchaseTotal,COALESCE(SUM(CASE WHEN status='completed' THEN total_cents ELSE 0 END),0) revenue,COALESCE(SUM(CASE WHEN status='completed' AND paid_at>=datetime('now','-7 days') THEN total_cents ELSE 0 END),0) week,COALESCE(SUM(CASE WHEN status='completed' AND paid_at>=datetime('now','start of month') THEN total_cents ELSE 0 END),0) month,COALESCE(SUM(CASE WHEN status='completed' AND paid_at>=datetime('now','start of year') THEN total_cents ELSE 0 END),0) year,SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) completed FROM store_orders WHERE mode=?`).bind(mode()).first();const sold=await db().prepare("SELECT COUNT(*) count FROM store_order_items i JOIN store_orders o ON o.id=i.order_id WHERE o.status='completed' AND o.mode=?").bind(mode()).first();const refunds=await db().prepare('SELECT COALESCE(SUM(r.amount_cents),0) amount FROM store_refunds r JOIN store_orders o ON o.id=r.order_id WHERE o.mode=?').bind(mode()).first();const recent=await db().prepare('SELECT * FROM store_orders WHERE mode=? ORDER BY created_at DESC LIMIT 30').bind(mode()).all();return json({summary,sold,refunds,recent:recent.results,mode:mode()});}

export async function ownerResourceFile(request:Request){mutation(request);const user=await customer(request);if(!owner(user))throw new StoreError(403,'Owner access required.');const input=await body(request);if(typeof input.productId!=='string'||typeof input.format!=='string')throw new StoreError(400,'Choose a resource and file format.');let file=resourceFile(input.productId,input.format);
 if(!file&&input.format==='default'&&elaRelease.some(p=>p.id===input.productId)){
  const p=await db().prepare('SELECT storage_key FROM store_products WHERE id=? AND ready=1').bind(input.productId).first<{storage_key:string}>();
  const bucket=Reflect.get(env,'PAID_FILES') as R2Bucket|undefined;const stored=p?await bucket?.get(p.storage_key):null;
  if(stored)return new Response(stored.body,{headers:{'Content-Type':'application/zip','Content-Disposition':`attachment; filename="${input.productId}.zip"`,'Cache-Control':'private, no-store','X-Content-Type-Options':'nosniff'}});
 }
 if(!file)throw new StoreError(404,'Resource file not found.');return new Response(file.body,{headers:{'Content-Type':file.contentType,'Content-Disposition':`attachment; filename="${file.name}"`,'Cache-Control':'private, no-store','X-Content-Type-Options':'nosniff'}});}

export async function uploadOwnerFile(request:Request){
 mutation(request);const user=await customer(request);if(!owner(user))throw new StoreError(403,'Owner access required.');
 const id=new URL(request.url).searchParams.get('productId')||'';
 const spec=Object.hasOwn(elaFiles,id)?elaFiles[id as keyof typeof elaFiles]:null;
 const product=elaRelease.find(p=>p.id===id);
 if(!spec||!product)throw new StoreError(400,'Choose an approved PowerPoint package.');
 if(Number(request.headers.get('content-length')||0)>spec.bytes)throw new StoreError(413,'This file is larger than the approved package.');
 const reader=request.body?.getReader();if(!reader)throw new StoreError(400,'Choose a file.');
 const bytes=new Uint8Array(spec.bytes);let size=0;
 while(true){const {done,value}=await reader.read();if(done)break;if(size+value.length>spec.bytes){await reader.cancel();throw new StoreError(413,'This file is larger than the approved package.');}bytes.set(value,size);size+=value.length;}
 const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('');
 if(size!==spec.bytes||hash!==spec.sha256)throw new StoreError(422,'This is not the verified package. Select the prepared ZIP for this resource.');
 const bucket=Reflect.get(env,'PAID_FILES') as R2Bucket|undefined;if(!bucket)throw new StoreError(503,'Protected storage is unavailable.');
 await initialize();const key='products/ela/'+hash+'/'+spec.name;
 await bucket.put(key,bytes,{httpMetadata:{contentType:'application/zip'},customMetadata:{sha256:hash}});
 const saved=await bucket.head(key);if(!saved||saved.size!==spec.bytes)throw new StoreError(503,'Upload verification failed. The listing has not been activated.');
 await db().prepare('UPDATE store_products SET title=?,price_cents=?,approved=1,ready=1,metadata=?,storage_key=? WHERE id=?').bind(product.title,product.priceCents,JSON.stringify(product),key,id).run();
 return json({ready:true,productId:id,bytes:size,sha256:hash});
}
export async function ownerUploadStatus(){
 await initialize();const {results}=await db().prepare('SELECT id,ready,approved FROM store_products').all<{id:string;ready:number;approved:number}>();
 return elaRelease.map(p=>({...p,ready:results.some(x=>x.id===p.id&&x.ready===1&&x.approved===1)}));
}
