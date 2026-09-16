import AccountPortal from "../components/AccountPortal";
export const metadata={title:'Your Account | Saint Pierre Learning Resources',robots:{index:false,follow:false}};
export const dynamic="force-dynamic";
export default async function Account(){return <main className="portal-shell"><header className="portal-header"><a href="/">← Store</a></header><section className="portal-card"><p className="eyebrow">SAINT PIERRE ACCOUNT</p><h1>Log in or create an account</h1><p>Use your email and password directly on this website.</p><AccountPortal/></section></main>}
