"use client";
import { FormEvent, useEffect, useRef, useState } from "react";
import { bearerHeaders, createSupabaseClient } from "../../lib/supabase";
function useSubmit(url:string){
  const [message,setMessage]=useState(''),[busy,setBusy]=useState(false);
  const locked=useRef(false);
  async function submit(payload:Record<string,unknown>){
    if(locked.current)return false;
    locked.current=true;setBusy(true);setMessage('Sending…');
    try{
      const {data}=await createSupabaseClient().auth.getSession();
      if(!data.session){setMessage('Please log in to your store account first. For login problems, use the email contact above.');return false;}
      const res=await fetch(url,{method:'POST',headers:{'content-type':'application/json',...bearerHeaders(data.session.access_token)},body:JSON.stringify(payload)});
      const result:any=await res.json();
      setMessage(res.ok?(result.message||'Saved successfully.'):(result.error||'The request was not completed. Contact support if this continues.'));
      return res.ok;
    }catch{setMessage('The result could not be confirmed. Check your messages before resending.');return false;}
    finally{locked.current=false;setBusy(false);}
  }
  return {message,submit,busy};
}
export function SupportForm(){
  const {message,submit,busy}=useSubmit('/api/support');
  const [tickets,setTickets]=useState<any[]>([]),[historyStatus,setHistoryStatus]=useState('Loading your messages…');
  async function loadMessages(){
    try{
      const {data}=await createSupabaseClient().auth.getSession();
      if(!data.session){setHistoryStatus('Log in to view or send private support messages.');return;}
      const res=await fetch('/api/support',{headers:bearerHeaders(data.session.access_token)});
      if(!res.ok)throw new Error();
      const result:any=await res.json();setTickets(result.items||[]);setHistoryStatus('');
    }catch{setHistoryStatus('Your message history could not load. Use Refresh messages to try again.');}
  }
  useEffect(()=>{void loadMessages()},[]);
  const onSubmit=async(e:FormEvent<HTMLFormElement>)=>{e.preventDefault();const form=e.currentTarget,f=new FormData(form);if(await submit({subject:f.get('subject'),message:f.get('message')})){form.reset();await loadMessages();}};
  return <><p><a href='/account'>Log in to your account</a></p><form className='portal-form' onSubmit={onSubmit}><label>What went wrong?<input name='subject' required maxLength={120}/></label><label>Tell us what happened<textarea name='message' required minLength={10} maxLength={2000} rows={6}/></label><button disabled={busy}>{busy?'Sending…':'Send support message'}</button><p aria-live='polite'>{message}</p></form><section className='review-list'><h2>Your support messages</h2><button className='portal-button' onClick={loadMessages}>Refresh messages</button><p role='status'>{historyStatus}</p>{!historyStatus&&!tickets.length&&<p>No support messages yet.</p>}{tickets.map(t=><article key={t.id}><h3>{t.subject}</h3><p>{t.status} · {t.createdAt}</p><p>{t.message}</p>{t.ownerReply?<blockquote><strong>Saint Pierre reply:</strong> {t.ownerReply}</blockquote>:<p>Awaiting a reply.</p>}</article>)}</section></>;
}
export function RequestForm(){
  const {message,submit,busy}=useSubmit('/api/requests');
  const onSubmit=async(e:FormEvent<HTMLFormElement>)=>{e.preventDefault();const form=e.currentTarget,f=new FormData(form);if(await submit(Object.fromEntries(f)))form.reset();};
  return <form className='portal-form' onSubmit={onSubmit}><p><a href='/account'>Log in</a> to send a private resource request.</p><div className='form-row'><label>Grade or course<input name='grade' required maxLength={80}/></label><label>Subject<input name='subject' required maxLength={80}/></label></div><label>State, if K–12<input name='state' maxLength={60}/></label><label>Describe the resource you need<textarea name='details' required minLength={10} maxLength={2000} rows={6}/></label><button disabled={busy}>{busy?'Sending…':'Submit resource request'}</button><p aria-live='polite'>{message}</p></form>;
}
export function FollowButton(){
  const {message,submit,busy}=useSubmit('/api/follow'),[active,setActive]=useState<boolean|null>(null),[status,setStatus]=useState('Loading follow preference…');
  useEffect(()=>{let mounted=true;createSupabaseClient().auth.getSession().then(async({data})=>{if(!data.session)throw new Error();const r=await fetch('/api/follow',{headers:bearerHeaders(data.session.access_token)});if(!r.ok)throw new Error();const d:any=await r.json();if(mounted){setActive(d.active===true);setStatus('')}}).catch(()=>{if(mounted)setStatus('Your follow preference could not load. Refresh to try again.')});return()=>{mounted=false}},[]);
  return <div><p>Save your interest in future resources. Automatic email updates are not enabled yet.</p><button className='portal-button' disabled={busy||active===null} onClick={async()=>{const next=!active;if(await submit({active:next}))setActive(next)}}>{busy?'Saving…':active?'Unfollow store':'Follow new resources'}</button><p aria-live='polite'>{message||status}</p></div>;
}
export function ReviewForm(){
  const {message,submit,busy}=useSubmit('/api/reviews'),[items,setItems]=useState<any[]>([]),[products,setProducts]=useState<{id:string;title:string}[]>([]),[slug,setSlug]=useState(''),[reviewStatus,setReviewStatus]=useState('Choose a resource to see its reviews.'),[catalogStatus,setCatalogStatus]=useState('Loading resources…');
  useEffect(()=>{fetch('/api/store/catalog').then(async r=>{if(!r.ok)throw new Error();return r.json() as Promise<{products:{id:string;title:string}[]}>}).then(d=>{setProducts(d.products||[]);setCatalogStatus(d.products?.length?'':'No resources are listed for review yet.')}).catch(()=>setCatalogStatus('Resources could not load. Refresh to try again.'))},[]);
  useEffect(()=>{let mounted=true;setItems([]);if(!slug){setReviewStatus('Choose a resource to see its reviews.');return;}setReviewStatus('Loading reviews…');fetch('/api/reviews?product='+encodeURIComponent(slug)).then(async r=>{if(!r.ok)throw new Error();return r.json() as Promise<{items:any[]}>}).then(d=>{if(mounted){setItems(d.items||[]);setReviewStatus('')}}).catch(()=>{if(mounted)setReviewStatus('Reviews could not load. Refresh to try again.')});return()=>{mounted=false}},[slug]);
  const onSubmit=async(e:FormEvent<HTMLFormElement>)=>{e.preventDefault();const form=e.currentTarget,f=new FormData(form);if(await submit({productSlug:slug,rating:Number(f.get('rating')),body:f.get('body')}))form.reset();};
  return <><form className='portal-form' onSubmit={onSubmit}><p><a href='/account'>Log in</a> to write a review. Reviews are moderated and are not labeled as verified purchases.</p><p role='status'>{catalogStatus}</p><label>Resource<select value={slug} required onChange={e=>setSlug(e.target.value)}><option value=''>Choose a resource</option>{products.map(p=><option key={p.id} value={p.id}>{p.title}</option>)}</select></label><label>Rating<select name='rating' defaultValue='5'>{[5,4,3,2,1].map(n=><option key={n} value={n}>{n} {n===1?'star':'stars'}</option>)}</select></label><label>Your review<textarea name='body' required minLength={5} maxLength={1200} rows={5}/></label><button disabled={busy||!slug}>{busy?'Sending…':'Submit review'}</button><p aria-live='polite'>{message}</p></form><div className='review-list'><p role='status'>{reviewStatus}</p>{!reviewStatus&&!items.length?<p>No approved reviews yet.</p>:items.map(x=><article key={x.id}><strong>{'★'.repeat(x.rating)} {x.displayName}</strong><p>{x.body}</p>{x.ownerReply&&<blockquote><b>Saint Pierre reply:</b> {x.ownerReply}</blockquote>}</article>)}</div></>;
}
