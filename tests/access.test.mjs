import {test,after} from 'node:test';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {build}=createRequire(require.resolve('wrangler/package.json'))('esbuild');
const ownerId='5bc573b8-0ce8-4933-b99f-2fa786ddcbd3';
globalThis.__accessFixture={user:null,selection:null,db:{}};
const fixture=globalThis.__accessFixture;
const row={id:1,userId:'private-user-id',email:'private@example.test',displayName:'private@example.test',rating:5,body:'Useful resource',ownerReply:'Thank you',createdAt:'2026-09-14'};
fixture.db={
  insert(){return {values(){return {onConflictDoUpdate:async()=>{}}}}},
  select(selection){fixture.selection=selection;const chain={from(){return chain},where(){return chain},orderBy(){return chain},limit:async()=>[Object.fromEntries(Object.keys(selection||row).map(k=>[k,row[k]]))]};return chain;},
};
const plugins=[{name:'access-fixture',setup(b){
  b.onResolve({filter:/^next\/server$/},()=>({path:'next',namespace:'fixture'}));
  b.onResolve({filter:/^cloudflare:workers$/},()=>({path:'env',namespace:'fixture'}));
  b.onResolve({filter:/^@supabase\/supabase-js$/},()=>({path:'supabase',namespace:'fixture'}));
  b.onResolve({filter:/\/db$/},()=>({path:'db',namespace:'fixture'}));
  b.onResolve({filter:/lib\/supabase$/},()=>({path:'config',namespace:'fixture'}));
  b.onLoad({filter:/.*/,namespace:'fixture'},a=>({loader:'js',contents:{
    next:'export const NextResponse={json:Response.json};',
    env:'export const env={DB:{prepare(){return {async all(){return {results:[]}}}}}};',
    config:"export const SUPABASE_URL='https://fixture.example.test';export const SUPABASE_PUBLISHABLE_KEY='fixture-public';",
    supabase:'export const createClient=()=>({auth:{getUser:async()=>({data:{user:globalThis.__accessFixture.user},error:null})}});',
    db:'export const getDb=()=>globalThis.__accessFixture.db;',
  }[a.path]}));
}}];
await build({entryPoints:{shared:'app/api/_shared.ts',reviews:'app/api/reviews/route.ts',owner:'app/api/owner/route.ts',support:'app/api/support/route.ts'},bundle:true,define:{'import.meta.env.VITE_STORE_PREVIEW':'"false"'},format:'esm',platform:'node',outdir:'.sites-runtime/tests/access',outExtension:{'.js':'.mjs'},plugins});
const shared=await import('../.sites-runtime/tests/access/shared.mjs');
const reviews=await import('../.sites-runtime/tests/access/reviews.mjs');
const owner=await import('../.sites-runtime/tests/access/owner.mjs');
const support=await import('../.sites-runtime/tests/access/support.mjs');
const request=(auth=false)=>new Request('https://store.example/api/owner',{headers:auth?{authorization:'Bearer fixture-token'}:{}});
function user(id,email='customer@example.test',confirmed=true){fixture.user={id,email,email_confirmed_at:confirmed?'2026-09-14':null,user_metadata:{}};}
after(()=>delete globalThis.__accessFixture);
test('anonymous visitors cannot retrieve owner inventory or support messages',async()=>{
  assert.equal((await owner.GET(request())).status,403);assert.equal((await support.GET(request())).status,401);
});
test('verified customer cannot gain ownership by using owner email or metadata',async()=>{
  user('another-id','ksaintpierre@lexcs.org');fixture.user.user_metadata={role:'owner'};
  assert.equal((await owner.GET(request(true))).status,403);
});
test('unconfirmed account is not treated as signed in',async()=>{
  user(ownerId,'owner@example.test',false);assert.equal(await shared.signedIn(request(true)),null);
});
test('verified existing owner can read inventory with no-store caching',async()=>{
  user(ownerId);const response=await owner.GET(request(true));assert.equal(response.status,200);
  assert.match(response.headers.get('cache-control'),/private, no-store/);
  const result=await response.json();assert.equal(result.powerPointDrafts.length,3);assert.equal(result.novelStudyDrafts.length,6);assert.equal(result.dailyDrafts.length,0);assert.equal(result.approvedResources.length,120);assert.ok(result.approvedResources.every(p=>p.approved===true));
});
test('public review projection excludes email and userId and removes email fallback names',async()=>{
  const result=await(await reviews.GET(new Request('https://store.example/api/reviews?product=example'))).json();
  assert.equal(fixture.selection.email,undefined);assert.equal(fixture.selection.userId,undefined);
  assert.equal(result.items[0].displayName,'Customer');assert.doesNotMatch(JSON.stringify(result),/private@example|private-user-id/);
});
test('signed-in profile does not default public display name to email',async()=>{
  user('another-id');const result=await shared.signedIn(request(true));assert.equal(result.displayName,'Customer');
});
