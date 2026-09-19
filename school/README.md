# Saint Pierre-Charles Online School

A self-paced, Pre-K–12 online school platform: a course catalog organized by
grade and subject, parent/student accounts, enrollment, and lesson-progress
tracking. This is a standalone Next.js app kept separate from the
`saintpierreresources.com` store elsewhere in this repository — it has its
own `package.json`, database, and deployment lifecycle, so it can be moved
into its own repository later with a simple copy.

## Stack

- Next.js 16 (App Router, Server Actions)
- SQLite via Drizzle ORM (`better-sqlite3`)
- Session auth: signed JWT cookie (`jose`) + `bcryptjs` password hashing
- Tailwind CSS v4

## Getting started

Requires Node.js 22+ and pnpm.

```sh
cd school
pnpm install
```

Create `.env.local` (or export these in your shell) with:

```
SCHOOL_SESSION_SECRET=some-long-random-string
```

Generate and apply the database schema, then seed sample data:

```sh
pnpm db:generate   # only needed after changing db/schema.ts
pnpm db:migrate
pnpm db:seed
```

Seeding creates an admin login (`admin@saintpierrecharles.school` /
`ChangeMe123!` — change this password before using in production) and a
handful of sample courses spanning Pre-K, Kindergarten, and grades 1, 3, 7,
and 10, so the catalog isn't empty on first run.

Run the dev server:

```sh
pnpm dev
```

Visit http://localhost:3000.

## How it's organized

- `db/schema.ts` — users (parent/admin), students, subjects, courses,
  lessons, enrollments, lesson progress.
- `app/courses` — public course catalog and course detail/enrollment.
- `app/lessons/[id]` — lesson viewer with a mark-complete action.
- `app/dashboard` — parent view: add student profiles, see enrollments and
  per-course progress.
- `app/admin` — admin-only course and lesson management (`middleware.ts`
  protects `/admin` by role and `/dashboard` by login).
- `app/signup`, `app/login`, `app/logout` — account creation and session
  management.

## Roadmap / not yet built

This is a first working slice, not the finished product. Deliberately left
out for now:

- **Payments** — no billing/tuition flow; enrollment is currently free.
- **Live classes** — no scheduling, video conferencing, or attendance;
  everything is self-paced.
- **Rich lesson content** — lessons currently hold plain text and an
  optional video link, not embedded video players, file uploads, or
  auto-graded quizzes.
- **Password reset / email verification** — signup and login are
  functional but there's no email flow yet.
- **Production database** — SQLite is fine for development; a hosted
  Postgres (or similar) is recommended before real users sign up.
