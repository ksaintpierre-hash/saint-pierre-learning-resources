'use client';
import {useState} from 'react';
import {bearerHeaders,createSupabaseClient} from '../../lib/supabase';

export default function OwnerResources({resources}:{resources:any[]}){
 const [query,setQuery]=useState(''),[message,setMessage]=useState(''),[busy,setBusy]=useState(false);
 const shown=resources.filter(p=>[p.title,p.level,p.subject,...p.collections].join(' ').toLowerCase().includes(query.toLowerCase()));
 async function download(productId:string,format:string){
  setBusy(true);setMessage('Preparing your file…');
  try{
   const {data}=await createSupabaseClient().auth.getSession();
   const response=await fetch('/api/store/owner-file',{method:'POST',headers:{...bearerHeaders(data.session?.access_token),'Content-Type':'application/json'},body:JSON.stringify({productId,format})});
   if(!response.ok){const result=await response.json() as {error?:string};throw new Error(result.error||'The file could not be downloaded.');}
   const filename=response.headers.get('Content-Disposition')?.match(/filename="([^"]+)"/)?.[1]||productId;
   const url=URL.createObjectURL(await response.blob());const anchor=document.createElement('a');anchor.href=url;anchor.download=filename;anchor.click();setTimeout(()=>URL.revokeObjectURL(url),30000);setMessage('Download started.');
  }catch(error){setMessage(error instanceof Error?error.message:'The download could not start.');}finally{setBusy(false);}
 }
 return <section className="owner-resources"><h2>Approved resource files</h2><p>{resources.length} approved resources with complete protected files. The approved release is activated automatically after publication. Customers receive full downloads only after verified payment.</p><label>Find a resource<input type="search" value={query} onChange={e=>setQuery(e.target.value)} placeholder="Title, grade, or collection"/></label><p role="status">{message}</p><div className="owner-resource-list">{shown.map(p=><article key={p.id}><div><h3>{p.title}</h3><p>{p.level} · {p.pages} main PDF pages{p.slides?` · ${p.slides} slides`:''}</p><a href={'/products/'+p.id}>View public listing and previews</a></div><div className="resource-download-actions"><button disabled={busy} onClick={()=>download(p.id,'pdf')}>Teaching PDF</button>{p.slides>0&&<><button disabled={busy} onClick={()=>download(p.id,'pptx')}>PowerPoint</button><button disabled={busy} onClick={()=>download(p.id,'slides')}>Slide PDF</button><button disabled={busy} onClick={()=>download(p.id,'default')}>Complete ZIP</button></>}</div></article>)}</div>{!shown.length&&<p>No resources match this search.</p>}</section>;
}
