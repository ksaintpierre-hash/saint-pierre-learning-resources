import OwnerDashboard from "../components/OwnerDashboard";
export const dynamic="force-dynamic";
export default async function Owner(){return <main className="portal-shell owner"><header className="portal-header"><a href="/">← Store</a><a href="/account">Account</a></header><OwnerDashboard/></main>}
