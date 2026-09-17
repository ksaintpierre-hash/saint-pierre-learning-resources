import { StoreHeader } from './components/Commerce';
import type { Metadata } from 'next';
export const metadata: Metadata = {title: 'Page Not Found | Saint Pierre Learning Resources', description: 'This page is not available. Browse our printable teaching resources for grades Pre-K through college.'};
export default function NotFound(){
  return <main className='commerce-shell'><StoreHeader/><section className='portal-card'><p className='eyebrow'>PAGE NOT AVAILABLE</p><h1>Let’s find the right resource.</h1><p>This link may be outdated, or the resource may not be available yet. Private drafts are not accessible from public links.</p><p><a className='portal-button' href='/#shop'>Browse resources</a></p><p>Already purchased something? Visit <a href='/purchases'>My Purchases</a> or <a href='/support'>contact support</a>.</p></section></main>;
}
