import { siteContent } from '../../server/editor';
export const dynamic='force-dynamic';
import { CheckCircle2, FileText, HeartHandshake, LockKeyhole, ShieldCheck } from "lucide-react";

export const metadata = {
  title: "Store Policies | Saint Pierre Learning Resources",
  description: "Privacy, licensing, refunds, accessibility, and standards policies for Saint Pierre Learning Resources.",
};

export default async function PoliciesPage() {
  const site=await siteContent();
  return <main className="policy-shell">
    <header className="portal-header policy-header">
      <a className="brand" href="/"><span className="brand-mark"><img src="/brand/saint-pierre-logo.png" alt=""/></span><span>Saint Pierre <small>Learning Resources</small></span></a>
      <a href="/">← Return to store</a>
    </header>
    {site.licenseText&&<section className="portal-card"><h2>Additional licensing information</h2><p>{site.licenseText}</p></section>}
    <section className="policy-hero">
      <p className="eyebrow"><ShieldCheck size={16}/> CUSTOMER CARE & STORE POLICIES</p>
      <h1>Clear expectations for every resource.</h1>
      <p>These policies explain how purchases, digital files, accounts, and customer support work. Effective September 13, 2026.</p>
      <nav aria-label="Policy sections"><a href="#license">License</a><a href="#refunds">Refunds</a><a href="#privacy">Privacy</a><a href="#accessibility">Accessibility</a><a href="#standards">Content promise</a><a href="#terms">Terms</a></nav>
    </section>

    <section className="policy-grid">
      <article id="license"><FileText/><h2>Digital Resource License</h2><p>Unless a listing says otherwise, each purchase includes a single-teacher license. The buyer may print and use the resource with their own students and may assign it through a password-protected classroom platform.</p><h3>Allowed</h3><ul><li>Classroom, tutoring, and personal instructional use</li><li>Reasonable copies for the purchasing teacher’s students</li><li>Posting inside a secure learning-management system for those students</li></ul><h3>Not allowed</h3><ul><li>Reselling, sharing, or giving the files to other educators</li><li>Posting files on a public website, shared drive, or social-media page</li><li>Removing the copyright notice or presenting the work as your own</li><li>Using the content to create a competing product</li></ul><p>Schools and teams that need multiple users should contact support for additional licensing.</p></article>

      <article id="refunds"><HeartHandshake/><h2>Refunds & Technical Support</h2><p>Because digital products can be accessed immediately, completed digital sales are generally final. We will still make things right when a customer receives the wrong file, cannot open a file, finds a material technical defect, or is charged twice.</p><ul><li>Report technical problems through the <a href="/support">Support Center</a>.</li><li>Include the purchase email, product title, and a description of the problem.</li><li>We may provide a corrected file, replacement access, or an appropriate refund after reviewing the issue.</li></ul><p>Customers should review the grade level, standard, file format, page count, and “What’s Included” section before purchasing.</p></article>

      <article id="privacy"><LockKeyhole/><h2>Privacy Notice</h2><p>We collect only information needed to operate the store, including account email and display name, support messages, resource requests, reviews, follows, basic visit information, and—after checkout is enabled—purchase and payment-confirmation details. Full card or bank information is handled by the payment provider and is not stored by this website.</p><h3>How information is used</h3><ul><li>Provide accounts, purchases, downloads, and customer support</li><li>Prevent misuse and maintain store security</li><li>Understand which resources and pages are useful</li><li>Respond to reviews and requested-resource submissions</li></ul><p>Service providers may process limited information to host the website, authenticate accounts, analyze visits, and process payments. We do not sell personal information. The store is intended for adult purchasers and is not designed to collect accounts directly from children under 13.</p><p>To request access, correction, or deletion of account information, use the <a href="/support">Support Center</a>.</p></article>

      <article id="accessibility"><CheckCircle2/><h2>Accessibility Statement</h2><p>Saint Pierre Learning Resources aims to make the website and products useful for a wide range of learners and educators. Product listings identify available supports for AIG, 504, EC, and ESL learners. We work toward readable type, clear headings, meaningful link text, keyboard-friendly website controls, useful image descriptions, and printable layouts with strong contrast.</p><p>If a website feature or purchased file creates an accessibility barrier, contact the <a href="/support">Support Center</a> and describe the product, page, and preferred format or accommodation.</p></article>

      <article id="standards"><ShieldCheck/><h2>Originality & Standards Promise</h2><p>Student passages, questions, activities, answer keys, and visual materials are created for Saint Pierre Learning Resources or used with documented permission. Official standards and released assessments may be researched to understand required skills and rigor, but released passages and questions are not copied into products.</p><ul><li>K–12 listings identify the state and verified standard when applicable.</li><li>Teacher notes cite the official standards source used during development.</li><li>College resources state a course level and objective without claiming accreditation or universal equivalency.</li><li>No certified Lexile measure is claimed unless an authorized certification exists.</li><li>Standards and testing programs can change; educators should also confirm local requirements.</li></ul></article>

      <article id="terms"><FileText/><h2>Website & Purchase Terms</h2><p>By creating an account or purchasing a product, customers agree to provide accurate information, use the website lawfully, protect their login details, and follow the product license. Product previews, descriptions, prices, and availability may change before purchase.</p><p>Educational resources support instruction but do not guarantee a particular grade, test score, certification, admission decision, or academic outcome. Customers remain responsible for deciding whether a resource fits their learners and local requirements.</p><p>The website may suspend accounts used for fraud, unauthorized file sharing, harmful activity, or repeated license violations. These terms are governed by applicable United States and North Carolina law. If any provision is unenforceable, the remaining provisions continue to apply.</p></article>
    </section>

    <section className="policy-contact"><h2>Need help or a different resource?</h2><p>Send a support message for an order or technical concern, or tell us what resource you need next.</p><div><a className="primary-button" href="/support">Contact support</a><a className="secondary-button" href="/requests">Request a resource</a></div></section>
    <footer className="policy-footer"><span>© 2026 Saint Pierre Learning Resources</span><a href="/">Store</a><a href="/account">Account</a><a href="/support">Support</a></footer>
  </main>;
}
