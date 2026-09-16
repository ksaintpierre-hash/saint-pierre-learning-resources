'use client';
import {useEffect,useRef,useState} from 'react';
import {bearerHeaders,createSupabaseClient} from '../../lib/supabase';

// Draft metadata arrives only from the owner-verified endpoint, never a public import.
export default function DailyDrafts({drafts}:{drafts:any[]}) {
 const [query,setQuery]=useState(''),[status,setStatus]=useState(''),[busy,setBusy]=useState(false);
 const [preview,setPreview]=useState<{url:string;alt:string}|null>(null);const urls=useRef<string[]>([]);
 useEffect(()=>()=>{urls.current.forEach(url=>URL.revokeObjectURL(url));},[]);
 async function file(id:string,format:'pdf'|'thumbnail',alt='') {
  setBusy(true);setStatus('Preparing private file…');
  try {
   const {data}=await createSupabaseClient().auth.getSession();
   const response=await fetch('/api/store/owner-file',{method:'POST',headers:{...bearerHeaders(data.session?.access_token),'Content-Type':'application/json'},body:JSON.stringify({productId:id,format})});
   if(!response.ok){const result=await response.json() as {error?:string};throw new Error(result.error||'Owner access is required.');}
   const url=URL.createObjectURL(await response.blob());urls.current.push(url);
   if(format==='thumbnail'){setPreview({url,alt});setStatus('Private cover preview loaded.');}
   else {const a=document.createElement('a');a.href=url;a.download=response.headers.get('Content-Disposition')?.match(/filename="([^"]+)"/)?.[1]||id+'.pdf';a.click();setStatus('Private download started.');}
  }catch(e){setStatus(e instanceof Error?e.message:'File unavailable. Please retry.');}finally{setBusy(false);}
 }
 const shown=drafts.filter(p=>[p.title,p.level,p.state,p.subject,p.standard].join(' ').toLowerCase().includes(query.toLowerCase()));
 return <section className="owner-resources"><h2>Daily private drafts · September 15, 2026</h2><p>{drafts.length} new resources awaiting your publication approval. Hidden from customers; checkout is inactive. Suggested prices are for review only.</p><label>Find a private draft<input type="search" value={query} onChange={e=>setQuery(e.target.value)} placeholder="Title, grade, state, or standard"/></label><p role="status">{status}</p>{preview&&<figure><img src={preview.url} alt={preview.alt} width="276" height="357" style={{maxWidth:'100%',height:'auto'}}/><figcaption>Private cover thumbnail—not customer-visible.</figcaption><button onClick={()=>setPreview(null)}>Close preview</button></figure>}<div className="owner-resource-list">{shown.map(p=><article key={p.id} style={{display:'block'}}><h3>{p.title}</h3><p>{p.level} · {p.state||'College / no state equivalency claim'} · {p.subject} · {p.pages} PDF pages · Suggested ${(p.priceCents/100).toFixed(2)}</p><p>{p.summary}</p><div className="resource-download-actions"><button disabled={busy} onClick={()=>file(p.id,'pdf')}>Download complete PDF</button><button disabled={busy} onClick={()=>file(p.id,'thumbnail',p.thumbnailAlt)}>View private cover</button></div><details><summary>Complete listing and review notes</summary><p>{p.detailedDescription}</p><h4>What’s included</h4><ul>{p.included.map((v:string)=><li key={v}>{v}</li>)}</ul><dl>{[['Standard / objective',p.standard+' — '+p.objective],['Resource type',p.resourceType],['Formats',p.formats.join(', ')+'; PNG thumbnail; no slides'],['Estimated time',p.minutes],['Student directions',p.studentDirections],['Teacher use',p.teacherUse],['Answer guidance',p.answerKey],['Preparation',p.preparation],['Printing',p.printing],['Digital use',p.digitalUse],['License',p.license],['Original content',p.originalContent],['Research notes',p.researchNotes],['Search tags',p.tags.join(', ')],['Thumbnail alt text',p.thumbnailAlt],['Publication status',p.publicationStatus]].map(([k,v])=><div key={k}><dt><strong>{k}</strong></dt><dd>{v}</dd></div>)}</dl><h4>Accessibility and differentiation</h4>{Object.entries(p.differentiation).map(([key,value])=><p key={key}><strong>{key}:</strong> {String(value)}</p>)}<h4>Sources</h4><ul>{p.sources.map((s:any)=><li key={s.url}><a href={s.url} target="_blank" rel="noreferrer">{s.title}</a> · accessed {s.accessed}</li>)}</ul></details></article>)}</div>{!shown.length&&<p>No private drafts match this search.</p>}</section>;
}
