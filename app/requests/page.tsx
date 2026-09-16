import { RequestForm } from "../components/PortalForms";
export const dynamic="force-dynamic";
export default async function Requests(){return <main className="portal-shell"><header className="portal-header"><a href="/">← Store</a><a href="/account">My account</a></header><section className="portal-card"><p className="eyebrow">RESOURCE REQUESTS</p><h1>What resource do you need?</h1><p>Request a grade, state, subject, language, PowerPoint, or college topic.</p><RequestForm/></section></main>}
