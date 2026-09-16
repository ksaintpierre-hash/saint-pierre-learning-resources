import { NextResponse } from "next/server";
import { getDb } from "../../../db";
import { events } from "../../../db/schema";
import { clean, signedIn } from "../_shared";
export async function POST(request:Request){
  const user=await signedIn(request), body=await request.json() as Record<string,unknown>;
  const eventType=clean(body.eventType,30), path=clean(body.path,200).split(/[?#]/)[0], productSlug=clean(body.productSlug,120);
  if(!["page_view","product_view","download_click"].includes(eventType)||!path.startsWith('/')||path.startsWith('//'))return NextResponse.json({error:"Invalid event"},{status:400});
  await getDb().insert(events).values({userId:user?.userId||null,eventType,path,productSlug:productSlug||null});
  return NextResponse.json({ok:true});
}
