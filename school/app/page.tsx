import Link from "next/link";

export default function HomePage() {
  return (
    <div className="flex flex-col gap-12">
      <section className="flex flex-col items-start gap-4">
        <h1 className="text-4xl font-bold text-[--color-brand]">
          A self-paced online school for Pre-K through 12th grade
        </h1>
        <p className="max-w-2xl text-lg text-black/70">
          Enroll your child in grade-level courses across every subject. Lessons, worksheets, and
          progress tracking your family can work through on your own schedule.
        </p>
        <div className="flex gap-3">
          <Link href="/courses" className="btn btn-primary">
            Browse courses
          </Link>
          <Link href="/signup" className="btn btn-secondary">
            Create a parent account
          </Link>
        </div>
      </section>

      <section className="grid gap-6 sm:grid-cols-3">
        <div className="card">
          <h2 className="font-semibold">Every grade band</h2>
          <p className="mt-2 text-sm text-black/60">
            Pre-K through 12th grade courses organized by subject and grade level.
          </p>
        </div>
        <div className="card">
          <h2 className="font-semibold">Learn at your own pace</h2>
          <p className="mt-2 text-sm text-black/60">
            Students work through lessons whenever it suits your family&apos;s schedule.
          </p>
        </div>
        <div className="card">
          <h2 className="font-semibold">Track progress</h2>
          <p className="mt-2 text-sm text-black/60">
            Parents can see which lessons each child has completed from one dashboard.
          </p>
        </div>
      </section>
    </div>
  );
}
