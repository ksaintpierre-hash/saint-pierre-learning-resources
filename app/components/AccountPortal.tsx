"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import { createSupabaseClient } from "../../lib/supabase";
import { FollowButton } from "./PortalForms";
import { authFeedback, passwordValidation } from "../../lib/auth-feedback";

const AUTH_RETURN_URL = "https://saintpierreresources.com/account";

export default function AccountPortal() {
  const supabase = useMemo(() => createSupabaseClient(), []);
  const [user, setUser] = useState<any>(null);
  const [mode, setMode] = useState<"login" | "signup" | "reset">("login");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [cooldown, setCooldown] = useState(0);
  const [recovering, setRecovering] = useState(false);

  useEffect(() => {
    const callback = new URLSearchParams(window.location.hash.slice(1));
    if(callback.has('error')) {
      setMessage(callback.get('error_code')==='otp_expired'
        ? 'This email link has expired or was already used. Try logging in with your latest password, or contact support for help. [email_link_expired]'
        : 'This email link could not be verified. Contact support for help. [email_link_invalid]');
      window.history.replaceState(null,'',window.location.pathname);
    }
    supabase.auth.getUser().then(({ data }) => { setUser(data.user); }).catch((error) => setMessage(authFeedback(error))).finally(() => setLoading(false));
    const { data } = supabase.auth.onAuthStateChange((event, session) => {
      setUser(session?.user || null);
      if (event === "PASSWORD_RECOVERY") setRecovering(true);
    });
    return () => data.subscription.unsubscribe();
  }, [supabase]);

  useEffect(() => {
    if (!cooldown) return;
    const timer = window.setInterval(() => setCooldown((seconds) => Math.max(0, seconds - 1)), 1000);
    return () => window.clearInterval(timer);
  }, [cooldown]);

  function changeMode(nextMode: "login" | "signup" | "reset") {
    setMode(nextMode);
    setMessage("");
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (submitting || ((mode === "signup" || mode === "reset") && cooldown > 0)) return;
    const form = new FormData(event.currentTarget);
    const email = String(form.get("email") || "").trim();
    const password = String(form.get("password") || "");
    const displayName = String(form.get("name") || "").trim();
    setSubmitting(true);
    setMessage("Please wait…");
    try {
      if (mode === "reset") {
        const { error } = await supabase.auth.resetPasswordForEmail(email, { redirectTo: AUTH_RETURN_URL });
        setCooldown(60);
        setMessage(error ? authFeedback(error) : "Request received. If this email has an eligible account, a reset link will be sent. Check inbox and spam. This message does not confirm delivery. If nothing arrives, contact support instead of repeatedly resending.");
        return;
      }
      const result = mode === "signup"
        ? await supabase.auth.signUp({ email, password, options: { data: { display_name: displayName }, emailRedirectTo: AUTH_RETURN_URL } })
        : await supabase.auth.signInWithPassword({ email, password });
      if (result.error) setMessage(authFeedback(result.error));
      else if (mode === "signup") {
        setCooldown(60);
        setMessage(result.data.session ? "You are logged in." : "Check your email for the next step. If you already have an account, use Log in. Contact support if no email arrives.");
      } else setMessage("You are logged in.");
    } catch (error) {
      setMessage(authFeedback(error));
    } finally {
      setSubmitting(false);
    }
  }

  async function setNewPassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (submitting) return;
    const formElement = event.currentTarget;
    const fields = new FormData(formElement);
    const password = String(fields.get("password") || "");
    const validation = passwordValidation(password, String(fields.get("confirmation") || ""));
    if (validation) { setMessage(validation); return; }
    setSubmitting(true);
    setMessage("Saving your new password…");
    try {
      const { error } = await supabase.auth.updateUser({ password });
      if (error) { setMessage(authFeedback(error)); return; }
      formElement.reset();
      setRecovering(false);
      setMessage("Your password was updated successfully. Use your new password the next time you log in.");
    } catch (error) { setMessage(authFeedback(error)); }
    finally { setSubmitting(false); }
  }

  async function changeAccountPassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (submitting) return;
    const formElement = event.currentTarget;
    const form = new FormData(formElement);
    const currentPassword = String(form.get("currentPassword") || "");
    const password = String(form.get("password") || "");
    const confirmation = String(form.get("confirmation") || "");
    const validation = passwordValidation(password, confirmation, currentPassword);
    if (validation) { setMessage(validation); return; }
    setSubmitting(true);
    setMessage("Saving your new password…");
    try {
      const { error } = await supabase.auth.updateUser({ current_password: currentPassword, password });
      if (error) { setMessage(authFeedback(error)); return; }
      formElement.reset();
      setMessage("Your password was changed successfully. Use your new password the next time you log in.");
    } catch (error) { setMessage(authFeedback(error)); }
    finally { setSubmitting(false); }
  }

  if (loading) return <p>Loading account…</p>;
  if (user && recovering) return <div className="auth-panel">
    <h2>Create your new password</h2>
    <p>Choose a unique password with at least 12 characters.</p>
    <form className="portal-form" onSubmit={setNewPassword}>
      <label>New password<input name="password" type="password" minLength={12} autoComplete="new-password" required /></label>
      <label>Confirm new password<input name="confirmation" type="password" minLength={12} autoComplete="new-password" required /></label>
      <button disabled={submitting}>{submitting ? "Saving…" : "Save new password"}</button>
      <p aria-live="polite">{message}</p>
    </form>
  </div>;

  if (user) return <>
    <div className="account-welcome"><h2>Welcome, {user.user_metadata?.display_name || user.email}</h2><p>{user.email}</p><button className="portal-button" disabled={submitting} onClick={async()=>{setSubmitting(true);try{const {error}=await supabase.auth.signOut();if(error)setMessage(authFeedback(error));else{setMessage('You are logged out.');setRecovering(false);}}catch(error){setMessage(authFeedback(error));}finally{setSubmitting(false);}}}>Log out</button></div>
    <section className="auth-panel" aria-labelledby="change-password-heading">
      <h2 id="change-password-heading">Change password</h2>
      <p>Use at least 12 characters for your new password. Enter it only here, never in a support message.</p>
      <form className="portal-form" onSubmit={changeAccountPassword}>
        <label>Current password<input name="currentPassword" type="password" autoComplete="current-password" required /></label>
        <label>New password<input name="password" type="password" minLength={12} autoComplete="new-password" required /></label>
        <label>Confirm new password<input name="confirmation" type="password" minLength={12} autoComplete="new-password" required /></label>
        <button disabled={submitting}>{submitting ? "Saving…" : "Change password"}</button>
      </form>
    </section>
    {message && <p aria-live="polite">{message}</p>}
    <p><a href="/owner">Store owner dashboard</a> · <a href="/support">Get account help</a></p>
    <section className="portal-grid"><article><h2>Your purchases</h2><a className="portal-button" href="/purchases">My Purchases</a><p>View your order status, purchased resources, and download history.</p></article><article><h2>Follow the store</h2><FollowButton /></article><article><h2>Support</h2><a className="portal-button" href="/support">Send a message</a></article><article><h2>Request a resource</h2><a className="portal-button" href="/requests">Make a request</a></article><article><h2>Reviews</h2><a className="portal-button" href="/reviews">Open reviews</a></article></section>
  </>;

  const emailActionLocked = (mode === "signup" || mode === "reset") && cooldown > 0;
  const buttonText = submitting ? "Please wait…" : emailActionLocked ? `Try again in ${cooldown}s` : mode === "login" ? "Log in" : mode === "signup" ? "Create account" : "Email reset link";
  return <div className="auth-panel">
    <div className="auth-tabs"><button onClick={() => changeMode("login")} aria-pressed={mode === "login"}>Log in</button><button onClick={() => changeMode("signup")} aria-pressed={mode === "signup"}>Create account</button><button onClick={() => changeMode("reset")} aria-pressed={mode === "reset"}>Reset password</button></div>
    <form className="portal-form" onSubmit={submit}>
      {mode === "signup" && <label>Name<input name="name" autoComplete="name" required /></label>}
      <label>Email<input name="email" type="email" autoComplete="email" required /></label>
      {mode !== "reset" && <label>{mode==='signup'?'Password (at least 12 characters)':'Password'}<input name="password" type="password" minLength={mode==='signup'?12:undefined} autoComplete={mode === "login" ? "current-password" : "new-password"} required /></label>}
      <button disabled={submitting || emailActionLocked}>{buttonText}</button>
      <p aria-live="polite">{message}</p>
    </form>
    <p><a href="/support">Having trouble logging in or receiving email?</a></p>
  </div>;
}
