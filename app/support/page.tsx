import { siteContent } from '../../server/editor';
import { SupportForm } from "../components/PortalForms";
const SUPPORT_EMAIL = 'ksaintpierre@lexcs.org';
export const dynamic="force-dynamic";
export default async function Support(){const site=await siteContent();return <main className="portal-shell"><header className="portal-header"><a href="/">← Store</a><a href="/account">My account</a></header><section className="portal-card"><p className="eyebrow">CUSTOMER SUPPORT</p><h1>How can we help?</h1>{site.supportText&&<p>{site.supportText}</p>}<p>For login or email-delivery problems, contact <a href={`mailto:${SUPPORT_EMAIL}`}>{SUPPORT_EMAIL}</a>. You do not need to log in to send email. Never include passwords, reset links, or payment details.</p><p>Signed-in customers can send a private message below and return here to read the store owner’s reply. Replies are not automatically emailed.</p><SupportForm/></section></main>}
