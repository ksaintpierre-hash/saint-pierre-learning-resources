"use client";
import { useEffect, useState } from "react";
import { CatalogItem, collectionsFor, gradesFor, matchesFilters } from "../lib/catalog-filters";
import { Check, ChevronDown, CreditCard, Download, FolderOpen, Map, Menu, Search, ShieldCheck, Sparkles, X } from "lucide-react";
import VisitTracker from "./components/VisitTracker";
import DailyLearningHub from './components/DailyLearningHub';

const categories = ["Subjects", "Grade Levels", "All 50 States", "Resource Types", "PowerPoints", "Sample Pages", "College"];
const resourceCollections = [
  ["EOG & State Test Prep","Original skill practice with verified standards and official assessment specifications."],
  ["Task Cards","Flexible practice cards for stations, review, intervention, and enrichment."],
  ["Warm-Ups","Focused opening activities designed for quick checks and strong lesson starts."],
  ["Classwork","Complete standards-aligned lessons and guided classroom practice."],
  ["Homework","Independent practice with clear directions and complete teacher keys."],
  ["Independent Work","Self-paced assignments with scaffolds and built-in accountability."],
  ["Small-Group Work","Targeted reteaching, intervention, language support, and enrichment."],
  ["Exit Tickets","Short mastery checks for the final minutes of a lesson."],
  ["Worksheets","Print-ready student pages with answer keys and differentiation guidance."],
  ["PowerPoints","Editable lesson slides, visuals, directions, and presentation-ready activities."],
  ["Sub Plans","Ready-to-use lessons that help learning continue during a planned absence."],
  ["Emergency Sub Plans","Low-prep, self-contained materials for unexpected absences."],
  ["Fall Packets","Seasonal skill practice for classrooms, tutoring, and home learning."],
  ["Winter Packets","Standards-focused winter practice with original content."],
  ["Spring Break Packets","Compact review and enrichment for the spring break period."],
  ["Summer Packets","Grade-level review and readiness practice for summer learning."],
  ["Lesson Plan Templates","Completed planning examples and reusable templates inside teaching bundles."],
  ["SAT Preparation","Focused original mathematics skill packets with worked solutions."],
  ["ACT Preparation","Focused original mathematics skill packets with worked solutions."],
  ["Classroom Management","Routines, procedures, planning tools, and practical teacher systems."],
  ["Classroom Décor","Original visual ideas and printable décor designed for useful classroom spaces."],
  ["Classroom Ideas","Organization, engagement, bulletin board, and learning-space inspiration."],
  ["Teacher Behavior Supports","Positive behavior tools, reflection forms, and intervention ideas."],
  ["Parent Behavior Supports","Practical home-school supports and family-friendly behavior tools."],
  ["New Teacher Tips","Actionable guidance, checklists, and planning support for new educators."],
  ["College Resources","General education core and introductory major-course practice."],
  ["World Languages","Spanish, French, German, Mandarin, ASL, and multilingual learning tools."],
  ["CTE & Career","Career and technical education, business, technology, and career-readiness materials."],
] as const;
const gradeLevels = ["All Levels","Pre-K","Kindergarten","Grade 1","Grade 2","Grade 3","Grade 4","Grade 5","Grade 6","Grade 7","Grade 8","Grade 9","Grade 10","Grade 11","Grade 12","College"];
const states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"];
const subjects = ["Math","Reading","Writing","Phonics","Grammar","Spelling","Science","Social Studies","CTE","Spanish","French","German","Art","Drama","Poetry","PowerPoints","College Core"];

import { defaultSite } from '../lib/editor-defaults';
export default function Home() {
  const [site,setSite]=useState(defaultSite);
  const [products,setProducts]=useState<CatalogItem[]>([]);
  const [catalogMessage,setCatalogMessage]=useState('Loading resources…');
  const countStatus=catalogMessage?(catalogMessage.startsWith('Loading')?'Loading count…':'Count unavailable'):null;
  const [liveOpen,setLiveOpen]=useState(false);
  useEffect(()=>{
    let active=true;
    fetch('/api/editor/site').then(r=>{if(!r.ok)throw new Error();return r.json() as Promise<typeof defaultSite>}).then(d=>{if(active)setSite({...defaultSite,...d})}).catch(()=>{});
    fetch('/api/store/catalog').then(async r=>{if(!r.ok)throw new Error();return r.json() as Promise<{products:CatalogItem[]}>}).then(d=>{if(active){setProducts(d.products||[]);setCatalogMessage('')}}).catch(()=>{if(active)setCatalogMessage('Resources could not load. Please refresh the page or contact Support.')});
    fetch('/api/store/configuration').then(r=>r.json() as Promise<{liveOpen:boolean}>).then(d=>{if(active)setLiveOpen(d.liveOpen===true)}).catch(()=>{});
    return()=>{active=false};
  },[]);
  const [menuOpen, setMenuOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [selectedCollection, setSelectedCollection] = useState("All Resources");
  const [selectedGrade, setSelectedGrade] = useState("All Levels");
  const [selectedState, setSelectedState] = useState("All States");
  const [selectedSubject,setSelectedSubject]=useState('All Subjects');
  const shown=products.filter(p=>matchesFilters(p,{grade:selectedGrade,state:selectedState,subject:selectedSubject,collection:selectedCollection,query}));
  const clearFilters=()=>{setSelectedCollection('All Resources');setSelectedGrade('All Levels');setSelectedState('All States');setSelectedSubject('All Subjects');setQuery('')};
  const isFiltered=selectedGrade!=='All Levels'||selectedState!=='All States'||selectedSubject!=='All Subjects'||selectedCollection!=='All Resources'||query.trim()!=='';
  return <main><VisitTracker/>
    <div className="announcement">{liveOpen?'SAINT PIERRE LEARNING RESOURCES':'STORE PREVIEW • BROWSE SAMPLES • PURCHASES ARE NOT OPEN YET'}</div>
    <header className="site-header">
      <a className="brand" href="#top" aria-label="Saint Pierre Learning Resources home"><span className="brand-mark"><img src="/brand/saint-pierre-logo.png" alt=""/></span><span>Saint Pierre <small>Learning Resources</small></span></a>
      <nav className={menuOpen ? "nav open" : "nav"} aria-label="Main navigation">{site.navigation.map((n,i)=><a key={i} href={n.url} onClick={()=>setMenuOpen(false)}>{n.label}</a>)}</nav>
      <button className="menu-button" onClick={()=>setMenuOpen(!menuOpen)} aria-label="Toggle menu" aria-expanded={menuOpen}>{menuOpen ? <X/> : <Menu/>}</button>
    </header>
    <section className="hero" id="top">
      <div className="hero-copy"><p className="eyebrow"><Sparkles size={16}/> PRINTABLE PRACTICE • TEACHER GUIDANCE</p><h1>{site.heroTitle}<br/><em>{site.heroAccent}</em></h1><p className="hero-text">{site.heroText}</p><div className="hero-actions"><a className="primary-button" href={site.buttonUrl}>{site.buttonLabel}</a><a className="text-link" href="#daily">Visit the daily hub <span>→</span></a></div><div className="trust-row"><span><Check size={17}/> Actual page previews</span><span><Check size={17}/> Clear formats & contents</span><span><Check size={17}/> Answer keys included</span></div></div>
      <a className="featured-resource" href="/products/fl-grade5-theme" aria-label="Explore Theme Detectives for Grade 5">
        <img src="/product-thumbnails/fl-grade5-theme.png?v=20260915b" alt="Theme Detectives cover: Evidence in Original Fiction, Grade 5 Florida" width="1160" height="1500"/>
        <div><span>EXPLORE A RESOURCE</span><strong>Theme Detectives</strong><p>Original fiction · Grade 5 · 6-page PDF</p><b>See the resource and sample →</b></div>
      </a>
    </section>
    <section className="category-strip" id="categories">{categories.map(c=><a key={c} href={c === "Grade Levels" ? "#grades" : c === "All 50 States" ? "#states" : c === "Resource Types" ? "#collections" : c==='Subjects'?'#subjects':"#shop"} onClick={()=>{if(c==='PowerPoints'){clearFilters();setSelectedCollection('PowerPoints')}if(c==='College'){clearFilters();setSelectedGrade('College')}}}>{c}<span>→</span></a>)}</section>
    <section className="shop-section" id="shop">
      <div className="section-heading"><div><p className="eyebrow">THE RESOURCE SHOP</p><h2>Made for your next lesson</h2>{isFiltered&&<div className="active-filter"><button onClick={clearFilters}>Clear all filters</button><p>{selectedGrade} · {selectedState} · {selectedSubject} · {selectedCollection}</p></div>}</div><label className="search"><Search size={19}/><input aria-label="Search resources" value={query} onChange={e=>setQuery(e.target.value)} placeholder="Title, skill, or standard"/></label></div>
      <div className="shop-controls"><label>Grade or course<select value={selectedGrade} onChange={e=>setSelectedGrade(e.target.value)}>{gradeLevels.filter(g=>g==='All Levels'||products.some(p=>gradesFor(p).includes(g))).map(g=><option key={g}>{g}</option>)}</select></label><label>Subject<select value={selectedSubject} onChange={e=>setSelectedSubject(e.target.value)}>{['All Subjects',...new Set(products.map(p=>p.subject))].map(v=><option key={v}>{v}</option>)}</select></label><p>PDFs and editable PowerPoints · Contents and availability shown per resource</p></div><p role="status">{catalogMessage||`${shown.length} matching resources`}</p>
      <div className="product-grid">{shown.map(p=><article className="product-card" key={p.id}><a className="product-image-frame" href={`/products/${p.id}`} aria-label={`View ${p.title}`}><img width="1160" height="1500" loading="lazy" src={p.thumbnailSrc||`/product-thumbnails/${p.id}.png?v=20260915b`} alt={`${p.title} cover`}/></a><div className="product-info"><p>{p.subject} • {p.level}</p><h3>{p.title}</h3><p className="description">{p.description}</p><p className="resource-facts">{p.pages} pages · {p.formats.join(' + ')} · {p.minutes}</p><a className="sample-link" href={`/products/${p.id}#preview`}>Preview sample page</a><div className="product-footer"><strong>{(p.priceCents/100).toLocaleString('en-US',{style:'currency',currency:'USD'})}</strong><a className="portal-button" href={`/products/${p.id}`}>View resource</a></div><small>{liveOpen&&p.ready?'Download after verified payment.':'Preview only · Not available for purchase yet.'}</small></div></article>)}</div>{!catalogMessage&&shown.length===0&&<p className="empty">No listed resources match these filters. <button onClick={clearFilters}>Clear filters</button> or <a href="/requests">request a resource</a>.</p>}
    </section>
    <section className="grade-section" id="grades">
      <div className="section-heading"><div><p className="eyebrow">SHOP BY GRADE LEVEL</p><h2>Find the right level in one click</h2><p>Choose a grade to find student materials and clearly labeled educator planning tools.</p></div></div>
      <div className="grade-level-grid">{gradeLevels.map(grade=><button key={grade} aria-pressed={selectedGrade===grade} className={selectedGrade===grade?"grade-level-card active":"grade-level-card"} onClick={()=>{clearFilters();setSelectedGrade(grade);document.getElementById("shop")?.scrollIntoView({behavior:"smooth"})}}><strong>{grade}</strong><span>{countStatus||`${products.filter(p=>grade==='All Levels'||gradesFor(p).includes(grade)).length} listed resources →`}</span></button>)}</div>
      <p className="catalog-note">Grade selections include student materials and clearly labeled educator planning tools. Complete bundles may appear in more than one collection when they include the relevant materials.</p>
    </section>
    <section className="collections-section" id="collections">
      <div className="section-heading"><div><p className="eyebrow"><FolderOpen size={16}/> SHOP BY RESOURCE TYPE</p><h2>A section for every classroom need</h2><p>Explore a focused collection, then filter the shop to see matching resources.</p></div></div>
      <div className="collection-grid">{[...resourceCollections.filter(([title])=>!site.collections.some(c=>c.title===title)),...site.collections.map(c=>[c.title,c.description])].map(([title,description])=><button key={title} aria-pressed={selectedCollection===title} className={selectedCollection===title?"collection-card active":"collection-card"} onClick={()=>{clearFilters();setSelectedCollection(title); document.getElementById("shop")?.scrollIntoView({behavior:"smooth"})}}><span>{title}</span><small>{description}</small><b>{countStatus||`${products.filter(p=>collectionsFor(p).includes(title)).length} listed resources →`}</b></button>)}</div>
    </section>
    <section className="national-section" id="states">
      <div><p className="eyebrow"><Map size={16}/> NATIONWIDE STANDARDS</p><h2>Growing toward all 50 states.</h2><p>Choose a state to filter the listed resources. Some state and grade collections are still in development; an empty collection is not available for purchase.</p></div>
      <div className="state-picker"><label htmlFor="state">Select your state</label><select id="state" value={selectedState} onChange={e=>{setSelectedState(e.target.value);document.getElementById('shop')?.scrollIntoView({behavior:'smooth'})}}><option>All States</option>{states.map(state=><option key={state}>{state}</option>)}</select><p><strong>{selectedState}</strong> · Filters the resource shop below</p></div>
      <div className="subject-cloud" id="subjects" aria-label="Subject filters">{['All Subjects',...subjects.filter(s=>!['PowerPoints','College Core'].includes(s))].map(subject=><button key={subject} aria-pressed={selectedSubject===subject} onClick={()=>{clearFilters();setSelectedSubject(subject);document.getElementById('shop')?.scrollIntoView({behavior:'smooth'})}}>{subject}</button>)}</div>
    </section>
    {site.samplerFile&&<section className="shop-section"><h2>{site.samplerTitle||'Try a free sample'}</h2><a className="portal-button" href={'/api/editor/media?id='+site.samplerFile}>Download free sampler PDF</a></section>}<DailyLearningHub />
    <section className="about-section" id="about"><div className="about-badge">KSP<span>Teacher-created</span></div><div><p className="eyebrow">MEET THE CREATOR</p><h2>Resources made from real classroom experience.</h2><p>I’m Katia Saint Pierre, a middle school ELA teacher in North Carolina. I create clear, rigorous materials that help teachers stay organized and help every learner engage with grade-level reading.</p><p>Each resource is built with purposeful scaffolds, meaningful practice, and the kind of answer key a busy teacher actually needs.</p></div></section>
    <section className="features"><div><Download/><h3>Digital & print-ready</h3><p>Download completed purchases from My Purchases. Print student pages or share them within your private classroom platform.</p></div><div><ShieldCheck/><h3>Teacher-friendly</h3><p>Clear directions and complete answer keys.</p></div><div><Sparkles/><h3>Student-centered</h3><p>Rigorous tasks with thoughtful support.</p></div></section>
    <section className="store-care"><div><p className="eyebrow"><ShieldCheck size={16}/> SHOP WITH CONFIDENCE</p><h2>Clear listings. Original resources. Real support.</h2><p>Every product listing explains the grade or course level, verified standard or objective, file format, page or slide count, what is included, accessibility supports, and license before you buy.</p></div><div className="care-links"><a href="/policies#license"><strong>Single-teacher license</strong><span>Understand permitted classroom use →</span></a><a href="/policies#refunds"><strong>Technical support</strong><span>See how file problems are resolved →</span></a><a href="/policies#privacy"><strong>Privacy protection</strong><span>Learn what information is collected →</span></a><a href="/policies#standards"><strong>Content promise</strong><span>Read our originality and standards process →</span></a></div></section>
    <section className="faq-section" id="faq"><p className="eyebrow">QUESTIONS & POLICIES</p><h2>Good to know</h2>{[["How will I receive my purchase?","After PayPal confirms completed payment, log in and open My Purchases to download your files. Pending payments must complete before downloads become available."],["Can I share a resource with my team?","A purchase is licensed to one teacher. Contact support about additional licenses for colleagues or school-wide use."],["What is the refund policy?","Completed digital sales are generally final. Contact support for wrong files, technical defects, access problems, or duplicate charges; we review these for a correction, replacement access, or an appropriate refund. See Store Policies for details."]].map(([q,a])=><details key={q}><summary>{q}<ChevronDown/></summary><p>{a}</p></details>)}</section>
    <footer><div className="brand footer-brand"><span className="brand-mark"><img src="/brand/saint-pierre-logo.png" alt=""/></span><span>Saint Pierre <small>Learning Resources</small></span></div><p>Focused printable resources for school and introductory college learning.</p><div><a href="#shop">Shop</a><a href="#collections">Collections</a><a href="/account">Account</a><a href="/support">Support</a><a href="/requests">Requests</a><a href="/reviews">Reviews</a><a href="/policies">Policies</a></div><small>© 2026 Saint Pierre Learning Resources. All rights reserved.</small></footer>
  </main>;
}
