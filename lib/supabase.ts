import { PREVIEW_MODE } from "./preview-mode";
import { createClient } from "@supabase/supabase-js";

export const SUPABASE_URL = PREVIEW_MODE ? "https://preview-auth.invalid" : "https://yefrepyrsmvnsnstshej.supabase.co";
export const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_fTNEla7Tn6VVfTA8hO-0-w_BtkeNZhO";

let browserClient: ReturnType<typeof createClient> | undefined;
export function createSupabaseClient() {
  if (typeof window === 'undefined') return createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, { auth: { persistSession: false, autoRefreshToken: false } });
  return browserClient ??= createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY);
}

export function bearerHeaders(token?: string): Record<string,string> {
  return token ? { Authorization: `Bearer ${token}` } : {};
}
