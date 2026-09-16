import { test, after } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { authFeedback, passwordValidation } from '../lib/auth-feedback.ts';
import { matchesFilters } from '../lib/catalog-filters.ts';
const catalog=JSON.parse(await readFile(new URL('../data/catalog.json',import.meta.url),'utf8'));
const all={grade:'All Levels',state:'All States',subject:'All Subjects',collection:'All Resources',query:''};
test('exact grades do not confuse Grade 1 with Grade 10 or 11',()=>{
  const p={...catalog[0],level:'Grade 10 • California'};
  assert.equal(matchesFilters(p,{...all,grade:'Grade 1'}),false);
  assert.equal(matchesFilters(p,{...all,grade:'Grade 10'}),true);
});
test('state, subject, grade, query and collection filters are real intersections',()=>{
  assert.equal(catalog.filter(p=>matchesFilters(p,{...all,state:'Texas'})).length,1);
  assert.equal(catalog.filter(p=>matchesFilters(p,{...all,grade:'Grade 4',state:'Texas'})).length,0);
  assert.equal(catalog.filter(p=>matchesFilters(p,{...all,subject:'Math'})).length,2);
  assert.equal(catalog.filter(p=>matchesFilters(p,{...all,collection:'PowerPoints'})).length,0);
  assert.equal(catalog.filter(p=>matchesFilters(p,{...all,query:'place value California'})).length,1);
  assert.equal(catalog.filter(p=>matchesFilters(p,all)).length,10);
});
test('auth feedback distinguishes common failures without exposing raw errors',()=>{
  assert.match(authFeedback({code:'same_password'}),/already your current password/);
  assert.match(authFeedback({code:'over_email_send_rate_limit'}),/stop resending/);
  assert.match(authFeedback({code:'email_address_not_authorized'}),/email service/);
  assert.match(authFeedback({code:'current_password_invalid'}),/current password is incorrect/);
  assert.match(authFeedback({code:'session_expired'}),/log in again/);
  assert.match(authFeedback({code:'reauthentication_needed'}),/verified again/);
  assert.match(authFeedback({code:'weak_password'}),/stronger/);
  assert.doesNotMatch(authFeedback({message:'secret-password secret-token',code:'<script>secret-token'}),/secret|<script>/);
  assert.match(authFeedback({code:'unexpected_failure'}),/unexpected_failure/);
});
test('new password validation catches short, mismatched and unchanged values',()=>{
  assert.match(passwordValidation('short','short'),/12/);
  assert.match(passwordValidation('Long-Fake-Pass1','Different-Fake2'),/do not match/);
  assert.match(passwordValidation('Long-Fake-Pass1','Long-Fake-Pass1','Long-Fake-Pass1'),/different/);
  assert.equal(passwordValidation('Long-Fake-Pass1','Long-Fake-Pass1'),null);
});

// Execute the actual account component with isolated React/Supabase fixtures.
// No browser passwords, real accounts, email requests, or network calls are used.
const require=createRequire(import.meta.url);
const {build}=createRequire(require.resolve('wrangler/package.json'))('esbuild');
globalThis.__authFixture={states:[],index:0,client:{auth:{}},user:{email:'owner@example.test',user_metadata:{display_name:'Test owner'}}};
await build({entryPoints:['app/components/AccountPortal.tsx'],bundle:true,define:{'import.meta.env.VITE_STORE_PREVIEW':'"false"'},format:'esm',platform:'node',jsx:'automatic',outfile:'.sites-runtime/tests/account.mjs',plugins:[{name:'account-fixtures',setup(b){
  b.onResolve({filter:/^(react|react\/jsx-runtime)$/},a=>({path:a.path,namespace:'fixture'}));
  b.onResolve({filter:/lib\/supabase$/},()=>({path:'supabase',namespace:'fixture'}));
  b.onResolve({filter:/PortalForms$/},()=>({path:'forms',namespace:'fixture'}));
  b.onLoad({filter:/.*/,namespace:'fixture'},a=>({loader:'js',contents:a.path==='react'?`export const useEffect=()=>{}; export const useMemo=f=>f(); export function useState(initial){const f=globalThis.__authFixture;const i=f.index++;if(!(i in f.states))f.states[i]=i===0?f.user:i===3?false:initial;return [f.states[i],v=>f.states[i]=typeof v==='function'?v(f.states[i]):v];}`:a.path==='react/jsx-runtime'?`export const Fragment='fragment';export const jsx=(type,props)=>({type,props});export const jsxs=jsx;`:a.path==='supabase'?`export const createSupabaseClient=()=>globalThis.__authFixture.client;`:`export const FollowButton=()=>null;` }));
}}]});
const {default:AccountPortal}=await import('../.sites-runtime/tests/account.mjs');
const realFormData=globalThis.FormData;
after(()=>{globalThis.FormData=realFormData;delete globalThis.__authFixture;});
function findForm(node){if(!node)return null;if(Array.isArray(node))return node.map(findForm).find(Boolean);if(node.type==='form')return node;return findForm(node.props?.children);}
async function passwordAttempt({recovering=false,error=null,thrown=false}={}){
  const fixture=globalThis.__authFixture;fixture.states=[];fixture.index=0;fixture.states[6]=recovering;
  let resolve,reject,reset=0,payload;
  fixture.client.auth.updateUser=input=>{payload=input;return new Promise((a,b)=>{resolve=a;reject=b});};
  const form={fields:{currentPassword:'Old-Fake-Pass1',password:'New-Fake-Pass2',confirmation:'New-Fake-Pass2'},reset(){reset++}};
  globalThis.FormData=class{constructor(f){this.fields=f.fields}get(key){return this.fields[key]}};
  const handler=findForm(AccountPortal()).props.onSubmit;
  const event={preventDefault(){},currentTarget:form};
  const pending=handler(event);
  event.currentTarget=null; // React clears this after dispatch, before the async result.
  if(thrown)reject(new TypeError('Private debug details'));else resolve({error});
  await pending;globalThis.FormData=realFormData;
  return {reset,message:fixture.states[2],busy:fixture.states[4],recovering:fixture.states[6],payload};
}
test('password save succeeds even after React clears currentTarget',async()=>{
  const result=await passwordAttempt();assert.equal(result.reset,1);assert.equal(result.busy,false);
  assert.match(result.message,/changed successfully/);assert.equal(result.payload.current_password,'Old-Fake-Pass1');
});
test('recovery password save clears recovery mode and confirms success',async()=>{
  const result=await passwordAttempt({recovering:true});assert.equal(result.reset,1);assert.equal(result.recovering,false);
  assert.match(result.message,/updated successfully/);assert.equal(result.payload.current_password,undefined);
});
test('same-password rejection is actionable and does not clear fields',async()=>{
  const result=await passwordAttempt({error:{code:'same_password'}});assert.equal(result.reset,0);assert.equal(result.busy,false);assert.match(result.message,/already your current password/);
});
test('network failure releases saving state without a false success',async()=>{
  const result=await passwordAttempt({thrown:true});assert.equal(result.reset,0);assert.equal(result.busy,false);assert.match(result.message,/not confirmed/);assert.doesNotMatch(result.message,/Private debug/);
});
