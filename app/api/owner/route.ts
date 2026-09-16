import {ownerUploadStatus} from '../../../server/commerce';
import { NextResponse } from "next/server";
import { env } from "cloudflare:workers";
import { eq } from "drizzle-orm";
import { getDb } from "../../../db";
import { reviews, supportTickets } from "../../../db/schema";
import { clean, isStoreOwner, signedIn } from "../_shared";
import { novelStudyDrafts } from '../../../server/draft-inventory';
import approvedResources from '../../../data/sales-release-2026-09-15.json';
import historicalDailyDrafts from '../../../server/daily-drafts-2026-09-15.json';
const releasedIds=new Set(approvedResources.map(p=>p.id));
const dailyDrafts=historicalDailyDrafts.filter(p=>!releasedIds.has(p.id));
async function rows(query:string){return (await env.DB!.prepare(query).all()).results}
export async function GET(request:Request){
  const user=await signedIn(request);
  if(!isStoreOwner(user))return NextResponse.json({error:"Owner access required"},{status:403});
  const [summary,tickets,requests,reviews,top]=await Promise.all([
    rows("SELECT (SELECT COUNT(*) FROM events WHERE event_type='page_view') visits,(SELECT COUNT(*) FROM followers WHERE active=1) followers,(SELECT COUNT(*) FROM orders WHERE status='completed') orders,(SELECT COALESCE(SUM(amount_cents),0) FROM orders WHERE status='completed') revenue,(SELECT COALESCE(SUM(amount_cents),0) FROM orders WHERE status='completed' AND created_at>=datetime('now','-7 days')) week,(SELECT COALESCE(SUM(amount_cents),0) FROM orders WHERE status='completed' AND created_at>=datetime('now','-1 month')) month,(SELECT COALESCE(SUM(amount_cents),0) FROM orders WHERE status='completed' AND created_at>=datetime('now','-1 year')) year"),
    rows("SELECT * FROM support_tickets ORDER BY created_at DESC LIMIT 20"),rows("SELECT * FROM resource_requests ORDER BY created_at DESC LIMIT 20"),rows("SELECT * FROM reviews ORDER BY created_at DESC LIMIT 20"),rows("SELECT product_slug,COUNT(*) views FROM events WHERE product_slug IS NOT NULL GROUP BY product_slug ORDER BY views DESC LIMIT 10")]);
  return NextResponse.json({summary:summary[0]||{},tickets,requests,reviews,top,powerPointDrafts:[],uploadResources:await ownerUploadStatus(),novelStudyDrafts,approvedResources,dailyDrafts},{headers:{'Cache-Control':'private, no-store'}});
}
export async function POST(request:Request){
  const user=await signedIn(request);
  if(!isStoreOwner(user))return NextResponse.json({error:"Owner access required"},{status:403});
  const body=await request.json() as Record<string,unknown>, action=clean(body.action,40), id=Number(body.id), reply=clean(body.reply,1200);
  if(!Number.isSafeInteger(id)||id<1||((action==='ticket_reply'||action==='review_reply')&&!reply))return NextResponse.json({error:'A valid item and a nonempty reply are required.'},{status:400});
  if(action==="ticket_reply")await getDb().update(supportTickets).set({ownerReply:reply,status:"resolved",updatedAt:new Date().toISOString()}).where(eq(supportTickets.id,id));
  else if(action==="review_reply")await getDb().update(reviews).set({ownerReply:reply,status:"approved"}).where(eq(reviews.id,id));
  else if(action==="approve_review")await getDb().update(reviews).set({status:"approved"}).where(eq(reviews.id,id));
  else return NextResponse.json({error:"Invalid action"},{status:400});
  return NextResponse.json({ok:true});
}
