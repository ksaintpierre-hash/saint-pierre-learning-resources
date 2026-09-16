import { NextResponse } from "next/server";
import { and, desc, eq } from "drizzle-orm";
import { getDb } from "../../../db";
import { reviews } from "../../../db/schema";
import { clean, signedIn } from "../_shared";

export async function GET(request:Request){
  const slug=new URL(request.url).searchParams.get("product")||"";
  // Public reviews must never expose account IDs or email addresses.
  const items=await getDb().select({id:reviews.id,displayName:reviews.displayName,rating:reviews.rating,body:reviews.body,ownerReply:reviews.ownerReply,createdAt:reviews.createdAt}).from(reviews).where(and(eq(reviews.productSlug,slug),eq(reviews.status,"approved"))).orderBy(desc(reviews.createdAt)).limit(100);
  return NextResponse.json({items:items.map(item=>({...item,displayName:item.displayName?.includes('@')?'Customer':item.displayName||'Customer'}))},{headers:{'Cache-Control':'no-store'}});
}
export async function POST(request:Request){
  const user=await signedIn(request);
  if(!user)return NextResponse.json({error:"Sign in required"},{status:401});
  const body=await request.json() as Record<string,unknown>, productSlug=clean(body.productSlug,120), text=clean(body.body,1200), rating=Number(body.rating);
  if(!productSlug||text.length<5||!Number.isInteger(rating)||rating<1||rating>5)return NextResponse.json({error:"Choose 1–5 stars and write a review."},{status:400});
  await getDb().insert(reviews).values({userId:user.userId,email:user.email,displayName:user.displayName,productSlug,rating,body:text});
  return NextResponse.json({ok:true,message:"Your review was sent for approval."});
}
