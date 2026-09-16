import { NextResponse } from "next/server";
import { getDb } from "../../../db";
import { followers } from "../../../db/schema";
import { signedIn } from "../_shared";
import { eq } from 'drizzle-orm';
export async function GET(request:Request){
  const user=await signedIn(request);
  if(!user)return NextResponse.json({error:'Sign in required'},{status:401});
  const rows=await getDb().select({active:followers.active}).from(followers).where(eq(followers.userId,user.userId)).limit(1);
  return NextResponse.json({active:rows[0]?.active===true},{headers:{'Cache-Control':'private, no-store'}});
}
export async function POST(request:Request){
  const user=await signedIn(request);
  if(!user)return NextResponse.json({error:"Sign in required"},{status:401});
  let body:{active?:unknown};try{body=await request.json()}catch{return NextResponse.json({error:'Invalid request'},{status:400})}
  if(body.active!==undefined&&typeof body.active!=='boolean')return NextResponse.json({error:'Invalid preference'},{status:400});
  const active=body.active!==false;
  await getDb().insert(followers).values({userId:user.userId,email:user.email,active}).onConflictDoUpdate({target:followers.userId,set:{email:user.email,active}});
  return NextResponse.json({ok:true,message:active?'You are following the store. You can unfollow here at any time.':'You have unfollowed the store.'});
}
