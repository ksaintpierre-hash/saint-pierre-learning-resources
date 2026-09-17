export default function Loading() {
  return (
    <main className="commerce-shell" aria-busy="true">
      <div className="loading-shell">
        <div className="loading-spinner" aria-hidden="true"/>
        <p>Loading&hellip;</p>
      </div>
    </main>
  );
}
