# Saint Pierre Learning Resources — launch review

Review date: September 14, 2026

## Decision: keep browsing available; do not open paid sales yet

This review corrected specific website defects and tested the changes. It is not a guarantee that every possible issue has been eliminated. Real email delivery, authenticated customer journeys, production fulfillment, and final teaching-file review remain launch gates.

## Repairs included in this version

| Area | Defect found | Repair |
|---|---|---|
| Password changes | React clears `event.currentTarget` before an awaited request completes. Resetting that reference could throw after a successful password update. | Capture the form before awaiting, show success only after the Auth response, and always release the saving state. Both account changes and recovery are covered by regression tests. |
| Authentication feedback | Different failures collapsed into a generic message; email request acceptance was presented as delivery. | Separate same-password, weak-password, current-password, expired-session, rate-limit, and connection messages. Display a safe error reference without raw passwords/tokens. Do not claim email delivery. |
| Account behavior | Multiple browser Auth clients, inconsistent password minimums, missing recovery confirmation, and unhandled sign-out failures. | Reuse one browser client, require confirmation for new recovery passwords, consistently require 12 characters for new passwords, preserve existing-password login, and handle sign-out failures. |
| Grade and state navigation | State selection did not filter products; prefix matching could mix Grade 1 with Grade 10. Subject links and some category shortcuts were inert. | Filter the actual approved catalog by exact grade, state, subject, collection, and search terms. Working clear-filters control, item counts, empty states, and request links. |
| Preview and availability | Listings could imply purchasable files despite unprepared delivery. | Honest preview-only labels, disabled add-to-cart for unprepared files, existing sample-page links, and an option to open larger sample images. |
| Review privacy | Public reviews selected whole records, including email and account ID; fallback display names could be emails. | Explicit public-field projection and removal of email fallback names. Moderated reviews are not represented as verified purchases. |
| Owner authorization | Owner access was based on email strings. | Bind owner authorization to the existing verified owner's immutable Auth user ID. A customer-supplied email/name/role cannot grant access. |
| Private drafts | Draft inventory titles were bundled in customer JavaScript; dashboard descriptions called them store-ready without final checks. | Move inventory to the authenticated owner endpoint; private, no-store responses; truthful pending-review labels. No new draft publication. |
| Customer support | Customers could submit a ticket but not see owner replies; login issues required login to ask for help. | Private ticket history, visible replies, refresh control, and a logged-out email contact. Explicitly state that support replies are not automatically emailed. |
| Owner replies | Network failures and duplicate submissions were poorly handled. | Locked submissions, bounded reply length, accurate success/failure feedback, and explicit review approval versus ticket resolution actions. |
| Follow and request forms | Follow had no customer-facing unfollow; request/review forms lacked useful pending states. | Read/save/unfollow preference, submission locks, field limits, dynamic review resource selection, and error states instead of falsely empty reviews. |
| Analytics | Product-view code was missing; counts could be mistaken for unique visitors. | Record product-view events, label page-view counts as non-unique, and strip query/fragment data from submitted analytics paths. |
| Content accuracy | A July 2021 IES report was incorrectly labeled a September 2026 release. The Texas product linked to an unrelated Biology source. | Clearly label the IES item as historical research and correct the Texas listing's source link. Flag the teacher PDF citation for correction before sale. |
| Presentation and recovery | Small text, inconsistent focus states, weak button contrast, and no branded missing-page/error fallback. | Readability and responsive CSS improvements, visible keyboard focus, stronger button contrast, and helpful missing-page/error screens. The official logo asset was preserved. |

## Verification performed

- TypeScript check: passed (`tsc --noEmit`).
- Production build: passed using the Sites build workflow.
- 28 automated tests passed: password form lifecycle, recovery mode, actionable errors, exact filters, owner/customer access separation, review privacy, anonymous configuration, private-product exclusion, unprepared-product rejection, server-side pricing, duplicate capture handling, invalid webhook rejection, refund access revocation, and expiring/single-use downloads.
- Tests used isolated mock Auth/PayPal responses and local D1/R2 fixtures. No real payments, customer accounts, reset emails, or production test orders were created.
- Browser preview: account form loaded; Grade 4 returned only the California Grade 4 item; Texas returned only the Texas item; sample images and logo loaded; support was reachable without login and explained private history; empty cart rendered without a false authentication error.
- Source/build inspection: no private draft inventory strings, paid PDF payloads, PayPal secret setting references, or owner ID appeared in the customer JavaScript scan.
- Read-only checks of the existing live domain returned HTTP 200 for home, account, support, reviews, requests, cart, purchases, policies, and catalog; anonymous owner and support API requests were denied (403/401). These checks were a baseline before deployment, not an authenticated purchase test.
- Browser console sampling showed a browser-extension error, not an application-origin exception in the sampled flow. This is not a complete cross-device accessibility or browser certification.

## Unfinished launch gates

1. **Real login and password change.** Katia must be able to sign in, change the password privately, log out, and sign in again with the new password. The code bug above is verified, but it does not prove the exact reason for every earlier authentication failure. No password was reset or disclosed during this review.
2. **Auth redirect and email service.** Verify Supabase Site URL and the exact allowed callback `https://saintpierreresources.com/account`; check confirmation/recovery templates and production SMTP delivery. The connected Supabase tools do not expose Auth configuration, SMTP settings, or delivery logs, so those settings were not changed or verified here. Test one signup and one recovery delivery to an authorized external mailbox; inspect failures instead of repeatedly resending. Do not disable email verification or use a shared password to bypass the problem.
3. **Secure product fulfillment.** The live catalog baseline contained ten listed products, all `ready: false`. Review the actual files, then prepare their private storage using authorized owner access. Confirm that every purchased file opens correctly and cannot be downloaded anonymously or by another customer. Do not expose full PDFs in public assets.
4. **PayPal end-to-end acceptance.** Complete a Sandbox journey with authorized test buyer/seller access: sign-in, cart, payment approval, server capture, webhook verification, My Purchases, download, cancellation, duplicate-submit protection, and refund/revocation. Automated simulations are not substitutes for this. Then obtain explicit approval for Live checkout.
5. **Content, branding, and licensing.** Final-review every resource's actual pages/slides, answers, quantities, previews, standards, logo placement, and third-party material rights. The private PowerPoint and novel inventory cards are not proof of completed delivery setup. In particular, correct the Texas teacher-guide citation before sale. This turn did not edit teaching PDFs/PPTX files or clear their publication gates.
6. **Operational readiness.** Test owner-to-customer support with two authorized accounts and establish who checks the support inbox. Automatic AI responses, notification emails, unique-visitor analytics, and background support monitoring are not enabled by these repairs. Verify mobile devices, keyboard/screen-reader flows, and backups before a broad launch.

## Verified source references

- [Supabase redirect URL configuration](https://supabase.com/docs/guides/auth/redirect-urls): production Site URL, allowed callback URLs, and confirmation/reset redirects.
- [Supabase custom SMTP guidance](https://supabase.com/docs/guides/auth/auth-smtp): production email setup. No conclusion is made here about which provider is currently configured.
- [Supabase authentication error codes](https://supabase.com/docs/guides/auth/debugging/error-codes): distinct authentication failures.
- [IES early-literacy research review](https://ies.ed.gov/use-work/resource-library/report/systematic-literature-review/effectiveness-early-literacy-instruction-summary-20-years-research): publication date July 2021, not September 2026.
- [Texas Education Agency TEKS Guide — Science 7.6A](https://teksguide.org/teks/s76a/overview): compare/contrast elements and compounds through atoms, molecules, symbols, and formulas. The standard code is valid; the previous PDF source citation was mismatched.

## Change boundaries

No payment settings, domain ownership, site audience, user passwords, or product publication approvals were changed. No real payment or purchase was made. Existing unapproved drafts remain private. Existing source and the prior archive were preserved; these repairs are recorded as a new version in the existing site's source repository.
