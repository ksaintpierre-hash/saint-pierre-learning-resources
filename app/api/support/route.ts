import { NextResponse } from "next/server";
import { desc, eq } from "drizzle-orm";
import { getDb } from "../../../db";
import { supportTickets } from "../../../db/schema";
import { clean, signedIn } from "../_shared";

export async function GET(request: Request) {
  const user = await signedIn(request);
  if (!user) return NextResponse.json({ error: "Sign in required" }, { status: 401 });
  const items = await getDb().select().from(supportTickets).where(eq(supportTickets.userId, user.userId)).orderBy(desc(supportTickets.createdAt));
  return NextResponse.json({ items }, {headers:{'Cache-Control':'private, no-store'}});
}

export async function POST(request: Request) {
  const user = await signedIn(request);
  if (!user) return NextResponse.json({ error: "Sign in required" }, { status: 401 });
  const body = await request.json() as Record<string,unknown>;
  const subject = clean(body.subject, 120), message = clean(body.message);
  if (!subject || message.length < 10) return NextResponse.json({ error: "Add a subject and at least 10 characters." }, { status: 400 });
  await getDb().insert(supportTickets).values({ userId:user.userId,email:user.email,subject,message });
  return NextResponse.json({ ok: true });
}
