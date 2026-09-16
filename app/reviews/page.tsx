import { ReviewForm } from "../components/PortalForms";
export const dynamic="force-dynamic";
export default async function Reviews(){return <main className="portal-shell"><header className="portal-header"><a href="/">← Store</a><a href="/account">My account</a></header><section className="portal-card"><p className="eyebrow">CUSTOMER REVIEWS</p><h1>Share your experience</h1><p>Reviews are checked before appearing publicly. The owner can reply.</p><ReviewForm/></section></main>}
