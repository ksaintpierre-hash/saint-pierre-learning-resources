"use client";
import { FormEvent, useRef, useState } from 'react';
import { bearerHeaders, createSupabaseClient } from '../../lib/supabase';
export default function OwnerActions({id,type}:{id:number;type:'ticket_reply'|'review_reply'}) {
  const [status,setStatus]=useState(''),[busy,setBusy]=useState(false),[saved,setSaved]=useState(false);
  const locked=useRef(false);
  async function submit(e:FormEvent<HTMLFormElement>) {
    e.preventDefault();if(locked.current)return;
    const f=new FormData(e.currentTarget);locked.current=true;setBusy(true);
    try{
      const {data}=await createSupabaseClient().auth.getSession();
      if(!data.session){setStatus('Log in again before replying.');return;}
      const r=await fetch('/api/owner',{method:'POST',headers:{'content-type':'application/json',...bearerHeaders(data.session.access_token)},body:JSON.stringify({action:type,id,reply:f.get('reply')})});
      if(!r.ok){setStatus('The reply was not saved. Refresh and try again.');return;}
      setSaved(true);setStatus(type==='ticket_reply'?'Reply saved in the customer’s support history. No email notification was sent.':'Reply saved and review approved.');
    }catch{setStatus('The result could not be confirmed. Refresh before retrying.');}
    finally{locked.current=false;setBusy(false);}
  }
  return <form className='inline-reply' onSubmit={submit}><label>Reply<textarea name='reply' required maxLength={1200} rows={2} disabled={saved}/></label><button disabled={busy||saved}>{busy?'Saving…':saved?'Saved':type==='ticket_reply'?'Reply & resolve':'Reply & approve'}</button><small role='status'>{status}</small></form>;
}
