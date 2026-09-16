'use client';
export default function SiteError({reset}:{reset:()=>void}){
  return <main className='commerce-shell'><section className='portal-card'><p className='eyebrow'>SAINT PIERRE LEARNING RESOURCES</p><h1>This page could not load.</h1><p>If you were submitting a payment or changing your password, its outcome is not confirmed. Check My Purchases or try signing in before submitting the same action again.</p><button className='portal-button' onClick={reset}>Reload this page</button><p><a href='/'>Return to store</a> · <a href='/purchases'>My Purchases</a> · <a href='/support'>Get help</a></p></section></main>;
}
