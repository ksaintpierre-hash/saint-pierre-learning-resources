'use client';
import {useState} from 'react';
import {bearerHeaders,createSupabaseClient} from '../../lib/supabase';
export default function OwnerUploads({resources}:{resources:any[]}){
 const [ready,setReady]=useState<string[]>(resources.filter(p=>p.ready).map(p=>p.id));
 const [busy,setBusy]=useState(false),[message,setMessage]=useState('');
 async function upload(id:string,file:File|undefined){
  if(!file)return;setBusy(true);setMessage('Uploading and verifying your package…');
  try{const {data}=await createSupabaseClient().auth.getSession();
   const res=await fetch('/api/store/owner-upload?productId='+encodeURIComponent(id),{method:'POST',headers:{...bearerHeaders(data.session?.access_token),'Content-Type':'application/zip'},body:file});
   const result:any=await res.json();if(!res.ok)throw new Error(result.error||'Upload failed.');
   setReady(old=>[...old,id]);setMessage('Package verified and available for sale.');
  }catch(e){setMessage(e instanceof Error?e.message:'Upload failed. Please try again.');}finally{setBusy(false);}
 }
 async function download(id:string){setBusy(true);setMessage('Preparing download…');try{
  const {data}=await createSupabaseClient().auth.getSession();const res=await fetch('/api/store/owner-file',{method:'POST',headers:{...bearerHeaders(data.session?.access_token),'Content-Type':'application/json'},body:JSON.stringify({productId:id,format:'default'})});
  if(!res.ok)throw new Error('The package could not be downloaded.');const url=URL.createObjectURL(await res.blob());const a=document.createElement('a');a.href=url;a.download=id+'.zip';a.click();setTimeout(()=>URL.revokeObjectURL(url),30000);setMessage('Download started.');
 }catch(e){setMessage(e instanceof Error?e.message:'Download failed.');}finally{setBusy(false);}}
 return <section className="owner-resources"><h2>Original Grade 7 PowerPoints</h2><p>Each verified ZIP includes the editable PowerPoint, a slide PDF, and teaching notes. A product becomes available for sale after its protected upload is verified.</p><p role="status">{message}</p><div className="owner-resource-list">{resources.map(p=><article key={p.id}><h3>{p.title}</h3><p>{p.slides} slides · ${(p.priceCents/100).toFixed(2)}</p>{ready.includes(p.id)?<><p>Available for sale</p><a href={'/products/'+p.id}>View product</a><button disabled={busy} onClick={()=>download(p.id)}>Download {p.title} ZIP</button></>:<label>Upload {p.title} ZIP<input type="file" accept=".zip,application/zip" disabled={busy} onChange={e=>upload(p.id,e.target.files?.[0])}/></label>}</article>)}</div></section>;
}
