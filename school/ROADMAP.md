# Roadmap

A working backlog for the Saint Pierre-Charles Online School. Items are
grouped by area and roughly ordered by priority within each group. Check
an item off (`[x]`) only once it's implemented, built successfully, and
smoke-tested — then log what changed in `PROGRESS.md`.

**Scope note on AIG / 504 / IEP / EC / ESL:** this platform tracks and
supports these designations operationally (accommodation flags,
differentiation, pacing, progress notes, language-support needs) so the
school can serve these students well day to day. It is **not** a legal
system of record for IEP or 504 compliance, nor for ESL/EL service-plan
compliance — families and the school still need their official
district/state paperwork for that. Don't build features that imply
otherwise (e.g. don't call anything here "the IEP" or generate documents
purporting to be legal IEPs or EL service plans).

## General curriculum build-out

- [ ] Full course library across ELA, Math, Science, and Social Studies for
      every grade band PK–12 (today only a sparse sample exists per grade)
- [ ] Course prerequisites/sequencing so a grade's courses form a coherent
      year, not just a loose bag of topics
- [ ] Auto-graded quizzes at the end of each lesson or unit
- [ ] Printable/downloadable worksheet attachments per lesson
- [ ] Parent-facing printable/exportable progress report per student per
      course

## Accessibility & 504 accommodation support

- [x] Student accommodation profile: AIG / 504 / EC-IEP / ESL-EL /
      extended-time flags + free-text accommodation notes (added, see
      PROGRESS.md)
- [ ] Lesson viewer: adjustable font size and a high-contrast display mode
- [ ] Optional text-to-speech playback for text-based lesson content
- [ ] When a student has `extendedTime` set, reflect it wherever timed
      work exists (not applicable yet — no timed assessments exist until
      the quiz feature above is built; revisit then)

## IEP / EC (Exceptional Children) support

- [ ] Per-student goal/progress notes an admin or parent can log over
      time, exportable as a simple report for an IEP meeting (informational
      only — see scope note above)
- [ ] Individualized pacing: let a parent/admin assign a student a modified
      subset of a course's lessons, or mark some as optional
- [ ] Admin view that lists all EC/IEP-flagged students across the school
      (today the flag exists per-student but has no admin-side rollup)

## English learner (ESL/EL) support

- [ ] Home-language field on the student profile, to inform which
      translated materials (if any) to surface
- [ ] Bilingual or simplified-English lesson text as an alternate view,
      starting with the highest-enrollment courses
- [ ] Admin rollup of ESL/EL-flagged students, mirroring the EC rollup above

## AIG / gifted enrichment

- [ ] "Enrichment" tag for courses that go above grade level, distinct from
      standard grade-level courses
- [ ] Confirm and, if needed, adjust enrollment so a gifted student can be
      enrolled in a course above their own grade band (the catalog nudges
      by grade but should not hard-block cross-grade enrollment)
- [ ] Admin rollup of AIG-identified students, mirroring the EC rollup above

## Parent experience

- [ ] Multiple parent/guardian accounts able to access the same student
      (co-parents/guardians both need visibility)
- [ ] Email notifications (course completed, weekly progress digest) —
      needs an email provider integration
- [ ] Family-level summary at the top of the dashboard when a parent has
      more than one child enrolled

## Payments

- [ ] Stripe Checkout so the listed course price is actually charged at
      enrollment (currently enrollment is free; price is display-only)
- [ ] Order/receipt history for parents
- [ ] Handle refunds/cancellations

## Platform hardening

- [ ] Password reset flow (currently no way to recover a forgotten password)
- [ ] Move from local SQLite to a hosted production database before real
      families sign up
- [ ] A basic automated test suite beyond manual/Playwright smoke checks,
      so future daily changes don't silently regress earlier features
- [ ] Rate limiting / basic abuse protection on signup and login
