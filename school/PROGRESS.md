# Progress log

Dated entries, newest first. Each entry should say what changed, why, and
how it was verified (build + smoke test, at minimum).

## 2026-09-19 (2)

Added an `isEnglishLearner` (ESL/EL) flag alongside the AIG/504/EC-IEP/
extended-time flags added earlier today — same treatment: capturable on
add/edit, shown as a dashboard badge. Added a matching "English learner
(ESL/EL) support" section to ROADMAP.md (home-language field, bilingual/
simplified-English lesson views, admin rollup). Verified with `pnpm build`
and a Playwright check that the badge appears after setting the flag.

## 2026-09-19

Added a student accommodation profile: `aigIdentified`, `has504Plan`,
`hasEcIep`, `extendedTime` booleans plus a free-text `accommodationNotes`
field on `students`. Captured on the "add student" form and editable via a
new `/dashboard/students/[id]/edit` page; shown as badges + notes on the
parent dashboard. Research (see conversation) showed extended time,
reduced-distraction settings, and flexible pacing are the most common
IEP/504 accommodations in virtual schools, and that NC's AIG program
requires differentiated services for identified gifted students — this
profile is the foundation both build on. Verified with `pnpm build` and an
8-check Playwright smoke test (add student with flags set → dashboard
badges appear → edit clears one flag and sets another → dashboard reflects
the change).
