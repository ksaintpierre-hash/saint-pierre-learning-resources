import { PREVIEW_MODE } from '../../lib/preview-mode';
import { getDb } from "../../db";
import { profiles } from "../../db/schema";
import { createClient } from "@supabase/supabase-js";
import { SUPABASE_PUBLISHABLE_KEY, SUPABASE_URL } from "../../lib/supabase";

// Bound to the existing verified owner, not a customer-editable email/name.
export const isStoreOwner = (user: { userId: string } | null) => user?.userId === '5bc573b8-0ce8-4933-b99f-2fa786ddcbd3';

export async function signedIn(request: Request) {
  if(PREVIEW_MODE)return null;
  const token = request.headers.get("authorization")?.replace(/^Bearer\s+/i, "");
  if (!token) return null;
  const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, { auth: { persistSession: false } });
  const { data, error } = await supabase.auth.getUser(token);
  const authUser = data.user;
  if (error || !authUser?.email || !authUser.email_confirmed_at) return null;
  const user = { userId: authUser.id, email: authUser.email, displayName: clean(authUser.user_metadata?.display_name,80) || 'Customer' };
  await getDb().insert(profiles).values({
    userId: user.userId,
    email: user.email,
    displayName: user.displayName,
  }).onConflictDoUpdate({
    target: profiles.userId,
    set: { email: user.email, displayName: user.displayName },
  });
  return user;
}

export function clean(value: unknown, max = 2000) {
  return typeof value === "string" ? value.trim().slice(0, max) : "";
}
