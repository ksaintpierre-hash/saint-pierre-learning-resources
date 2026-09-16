import { NextResponse } from "next/server";
import { getDb } from "../../../db";
import { resourceRequests } from "../../../db/schema";
import { clean, signedIn } from "../_shared";

export async function POST(request: Request) {
  const user = await signedIn(request);
  if (!user) return NextResponse.json({ error: "Sign in required" }, { status: 401 });
  const body = await request.json() as Record<string,unknown>;
  const grade=clean(body.grade,80), subject=clean(body.subject,80), state=clean(body.state,80), details=clean(body.details);
  if (!grade || !subject || details.length < 10) return NextResponse.json({ error:"Grade, subject, and details are required." },{status:400});
  await getDb().insert(resourceRequests).values({userId:user.userId,email:user.email,grade,subject,state:state||null,details});
  return NextResponse.json({ok:true});
}
