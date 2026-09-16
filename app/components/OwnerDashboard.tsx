"use client";
import { useEffect, useState } from "react";
import { bearerHeaders, createSupabaseClient } from "../../lib/supabase";
import { SalesDashboard } from "./Commerce";
import OwnerActions from "./OwnerActions";
import PowerPointDrafts from "./PowerPointDrafts";
import NovelStudyDrafts from "./NovelStudyDrafts";
import OwnerResources from './OwnerResources';
import DailyDrafts from './DailyDrafts';
import OwnerUploads from './OwnerUploads';

export default function OwnerDashboard() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    createSupabaseClient().auth.getSession().then(async ({ data: sessionData }) => {
      if (!sessionData.session) { setError("Log in to your store account first."); return; }
      const response = await fetch("/api/owner", { headers: bearerHeaders(sessionData.session.access_token) });
      const result: any = await response.json();
      if (!response.ok) setError(result.error || "Owner access required");
      else setData(result);
    }).catch(() => setError('The dashboard could not load. Your account has not been changed. Refresh or contact support.'));
  }, []);
  if (error) return <div className="portal-card"><h1>Owner dashboard</h1><p>{error}</p><a className="portal-button" href="/account">Owner login</a></div>;
  if (!data) return <p>Loading dashboard…</p>;
  const summary = data.summary;
  return <>
    <h1>Business overview</h1><p><a className="portal-button" href="/editor">Open visual editor →</a></p>
    <SalesDashboard />
    {data.dailyDrafts?.length>0&&<DailyDrafts drafts={data.dailyDrafts} />}
    <OwnerResources resources={data.approvedResources||[]} />
    <OwnerUploads resources={data.uploadResources||[]} />
    <NovelStudyDrafts drafts={data.novelStudyDrafts||[]} />
    <section className="metric-grid"><article><b>{summary.visits || 0}</b><span>Page views (not unique visitors)</span></article><article><b>{summary.followers || 0}</b><span>Followers</span></article></section>
    <section className="owner-sections">
      <div><h2>Support messages</h2>{data.tickets.length ? data.tickets.map((ticket: any) => <article key={ticket.id}><b>{ticket.subject}</b><small>{ticket.email + " • " + ticket.status}</small><p>{ticket.message}</p>{ticket.owner_reply ? <blockquote>{ticket.owner_reply}</blockquote> : <OwnerActions id={ticket.id} type="ticket_reply" />}</article>) : <p>No messages yet.</p>}</div>
      <div><h2>Resource requests</h2>{data.requests.length ? data.requests.map((request: any) => <article key={request.id}><b>{request.grade + " • " + request.subject}</b><small>{(request.state || "College/general") + " • " + request.email}</small><p>{request.details}</p></article>) : <p>No requests yet.</p>}</div>
      <div><h2>Reviews</h2>{data.reviews.length ? data.reviews.map((review: any) => <article key={review.id}><b>{"★".repeat(review.rating) + " • " + review.product_slug}</b><small>{review.email + " • " + review.status}</small><p>{review.body}</p>{review.owner_reply ? <blockquote>{review.owner_reply}</blockquote> : <OwnerActions id={review.id} type="review_reply" />}</article>) : <p>No reviews yet.</p>}</div>
      <div><h2>Most-viewed resources</h2>{data.top.length ? data.top.map((item: any) => <p key={item.product_slug}><b>{item.product_slug}</b>{" — " + item.views + " interactions"}</p>) : <p>No product activity yet.</p>}</div>
    </section>
  </>;
}
