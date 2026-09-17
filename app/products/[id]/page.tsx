import { notFound } from "next/navigation";
import { publicCatalog } from "../../../server/commerce";
import { AddToCart, StoreHeader } from "../../components/Commerce";
import pedagogy from '../../../data/pedagogy.json';
import VisitTracker from '../../components/VisitTracker';

export const dynamic = "force-dynamic";

export async function generateMetadata({params}:{params:Promise<{id:string}>}){
  const {id}=await params;
  const p=(await publicCatalog()).find(p=>p.id===id);
  if(!p)return{};
  const title=p.seoTitle||p.title+' | Saint Pierre Learning Resources';
  const description=p.seoDescription||p.description;
  const image='https://saintpierreresources.com'+(p.thumbnailSrc||'/product-thumbnails/'+p.id+'.png');
  return {
    title,
    description,
    openGraph:{title,description,url:'https://saintpierreresources.com/products/'+p.id,siteName:'Saint Pierre Learning Resources',images:[{url:image,width:1160,height:1500,alt:p.title+' cover'}],type:'website'},
    twitter:{card:'summary_large_image',title,description,images:[image]},
  };
}
export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const catalog = await publicCatalog();
  const p = catalog.find((product) => product.id === id);
  if (!p) notFound();
  const related=catalog.filter(x=>(p.relatedProducts||[]).includes(x.id));
  const bundle=catalog.filter(x=>(p.bundleProducts||[]).includes(x.id));
  const guide = pedagogy[p.id as keyof typeof pedagogy];
  const studentPage = p.id === 'fl-grade5-theme' ? 4 : 3;
  const sourceUrl = p.id === 'tx-grade7-elements-compounds'
    ? 'https://teksguide.org/teks/s76a/overview'
    : (p.source||'').match(/https:\/\/[^\s]+/)?.[0];
  const previews = p.previews || [{src:'/product-previews/'+p.id+'.png',alt:'Sample practice page from '+p.title,page:null}];
  return <main className="commerce-shell">
    <VisitTracker productId={p.id}/>
    <StoreHeader />
    <nav className="product-breadcrumb" aria-label="Breadcrumb"><a href="/#shop">Resource shop</a><span aria-hidden="true">/</span><span>{p.subject}</span></nav>
    <section className="product-detail">
      <img className="detail-cover" src={p.thumbnailSrc||"/product-thumbnails/" + p.id + ".png?v=20260915b"} alt={p.thumbnailAlt || p.title + " cover"} />
      <div>
        <p className="eyebrow">{p.level} · {p.subject}</p>
        <h1>{p.title}</h1>
        <p>{p.description}</p>{p.requiredBook&&<p className="notice"><strong>Required materials:</strong> {p.requiredBook}</p>}<dl className="purchase-facts"><div><dt>Formats</dt><dd>{p.formats.join(" + ")} · {p.pages} main pages{p.slides?` · ${p.slides} editable slides`:""}</dd></div><div><dt>Lesson time</dt><dd>{p.minutes}</dd></div><div><dt>Includes</dt><dd>Teacher guidance + answer guidance</dd></div></dl>
        {p.audience && <p><strong>For:</strong> {p.audience}</p>}
        <a className="preview-jump" href="#preview">Preview a sample page ↓</a>
        <p className="detail-price">{(p.priceCents / 100).toLocaleString("en-US", { style: "currency", currency: "USD" })} USD</p>
        <AddToCart id={p.id} ready={p.ready} />
        <p className="purchase-note">One-time purchase · Single-teacher license<br/>{p.formats.includes("PPTX")?"Printable PDFs and editable PowerPoint included.":"Printable PDF."} Account required for purchase and download.</p><a className="product-help" href="/support">Questions about this resource? Contact support.</a>
      </div>
    </section>
    {guide && <section className="lesson-fit"><div><h2>Is this the right fit?</h2><p>{guide.fit}</p></div><div><h2>Before students begin</h2><p>{guide.prerequisites}</p></div></section>}
    <section className="resource-preview" id="preview">
      <div>
        <p className="eyebrow">RESOURCE PREVIEW</p>
        <h2>See what you’re buying</h2>
        <p>{p.previewDescription || 'This sample shows an actual student-practice page. It is not the complete resource.'}</p>
        <p><a href={previews[0].src} target='_blank' rel='noreferrer'>Open a larger sample image ↗</a></p>
      </div>
      <figure className="preview-page">
        <img src={previews[0].src} alt={previews[0].alt} />
        <span aria-hidden="true">KSP PREVIEW</span>
        <figcaption><img className='preview-brand' src='/brand/saint-pierre-logo.png' alt='KSP Haitian-flag logo'/>Sample page · Preview only · © 2026 Saint Pierre Learning Resources</figcaption>
      </figure>
    </section>
    {previews.length>1 && <section className="additional-previews"><h2>More inside the resource</h2><div>{previews.slice(1).map((preview:any)=><figure key={preview.src}><a href={preview.src} target="_blank" rel="noreferrer"><img loading="lazy" src={preview.src} alt={preview.alt}/></a><figcaption>Actual page {preview.page} · Select to enlarge</figcaption></figure>)}</div></section>}
    {bundle.length>0&&<section className="detail-grid"><article><h2>Resources in this bundle</h2><ul>{bundle.map(x=><li key={x.id}><a href={'/products/'+x.id}>{x.title}</a></li>)}</ul></article></section>}
    <section className="detail-grid">
      <article>
        {p.detailedDescription && <><h2>How this resource helps</h2><p>{p.detailedDescription}</p></>}
        <h2>What’s Included</h2>
        <ul>{p.included.map((x: string) => <li key={x}>{x}</li>)}</ul>
        {guide && <><h2>Inside the PDF</h2><ol className="page-map"><li><span>Page 1</span>Cover</li><li><span>Page 2</span>Teacher guide, model, and learning supports</li>{p.id==='fl-grade5-theme'&&<li><span>Page 3</span>Original story: The Garden Sign</li>}<li><span>Page {studentPage}</span>Eight practice tasks</li><li><span>Page {studentPage+1}</span>Two skill-specific exit tasks and reflection</li><li><span>Page {studentPage+2}</span>Answer key and next teaching steps</li></ol></>}
        <h2>Resource details</h2>
        <dl><dt>Grade / course</dt><dd>{p.level}</dd>{p.state&&<><dt>State / alignment scope</dt><dd>{p.state}</dd></>}<dt>Subject and resource type</dt><dd>{p.subject} · {p.resourceType}</dd><dt>Files</dt><dd>{p.pages} main PDF pages{p.additionalPdfPages?` + ${p.additionalPdfPages} slide-handout pages`:''}{p.slides?` · ${p.slides} editable slides`:''} · {p.formats.join(' + ')}{p.distributionFormat==='ZIP'?' in one ZIP download':''}</dd><dt>Estimated completion time</dt><dd>{p.minutes}</dd><dt>Answer key</dt><dd>{p.answerKey||'Fixed-response answers and guidance for open-ended tasks are included.'}</dd></dl>
        <h2>Standard or objective</h2><p>{p.standard}</p>{p.objective&&<p>{p.objective}</p>}{p.sources?<ul>{p.sources.map((s:any)=><li key={s.url}><a href={s.url} target="_blank" rel="noreferrer">{s.title} ↗</a></li>)}</ul>:sourceUrl?<p><a href={sourceUrl} target='_blank' rel='noreferrer'>Official standards source ↗</a></p>:<p>{p.source}</p>}{p.accessedAt&&<p>Sources checked {p.accessedAt}.</p>}
        {p.studentDirections&&<><h2>Learner directions</h2><p>{p.studentDirections}</p></>}
        {p.teacherUse&&<><h2>Teaching suggestions</h2><p>{p.teacherUse}</p></>}
      </article>
      <article>
        <h2>Learning supports</h2>
        <p><strong>AIG:</strong> {p.accessibility?.AIG||guide?.supports['AIG']||'Second methods, counterexamples, transfer tasks, and student-designed extensions.'}</p>
        <p><strong>504:</strong> {p.accessibility?.['504']||guide?.supports['504']||'Chunked pages, extended time, reduced copying, and breaks according to the learner’s plan.'}</p>
        <p><strong>EC:</strong> {p.accessibility?.EC||guide?.supports['EC']||'Vocabulary previews, modeled items, visuals, manipulatives, and oral responses when appropriate to the IEP.'}</p>
        <p><strong>ESL:</strong> {p.accessibility?.ESL||guide?.supports['ESL']||'Key-term previews, sentence frames, bilingual glossaries, and partner rehearsal.'}</p>
        <h2>Printing and preparation</h2><p>{p.preparation||'Print on US Letter paper at actual size. Separate student practice and assessment from the teacher guide and key. Review the model and prepare needed support materials.'}</p>{p.digitalNotes&&<p>{p.digitalNotes}</p>}
        {p.originality&&<><h2>Original content</h2><p>{p.originality}</p></>}
        <h2>License</h2><p>{p.license||'For one teacher’s own classroom use. Do not resell, redistribute files, or post them publicly.'} See the <a href="/policies#license">full license</a>.</p>
        {p.tags&&<><h2>Search tags</h2><p>{p.tags.join(' · ')}</p></>}
        {p.publicationStatus&&<p className="notice">{p.publicationStatus}</p>}
      </article>
    </section>
    {related.length>0&&<section className="detail-grid"><article><h2>You may also like</h2><ul>{related.map(x=><li key={x.id}><a href={'/products/'+x.id}>{x.title}</a> · ${(x.priceCents/100).toFixed(2)}</li>)}</ul></article></section>}
    <script type="application/ld+json" dangerouslySetInnerHTML={{__html:JSON.stringify({
      "@context":"https://schema.org",
      "@type":"Product",
      "name":p.title,
      "description":p.description,
      "image":"https://saintpierreresources.com"+(p.thumbnailSrc||"/product-thumbnails/"+p.id+".png"),
      "url":"https://saintpierreresources.com/products/"+p.id,
      "brand":{"@type":"Brand","name":"Saint Pierre Learning Resources"},
      "offers":{"@type":"Offer","priceCurrency":"USD","price":(p.priceCents/100).toFixed(2),"availability":"https://schema.org/InStock","seller":{"@type":"Organization","name":"Saint Pierre Learning Resources"}},
      "audience":{"@type":"EducationalAudience","educationalRole":p.audience||"student"},
      "educationalLevel":p.level,
      "teaches":p.standard,
    })}}/>
  </main>;
}
