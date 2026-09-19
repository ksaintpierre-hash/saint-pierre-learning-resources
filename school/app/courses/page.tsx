import Link from "next/link";
import { and, eq } from "drizzle-orm";
import { db } from "@/db";
import { courses, subjects } from "@/db/schema";
import { GRADE_LEVELS, gradeLabel, type GradeLevel } from "@/lib/grades";

export default async function CoursesPage({
  searchParams,
}: {
  searchParams: Promise<{ grade?: string; subject?: string }>;
}) {
  const { grade, subject } = await searchParams;

  const allSubjects = await db.select().from(subjects).orderBy(subjects.name);

  const filters = [];
  if (grade && GRADE_LEVELS.includes(grade as GradeLevel)) {
    filters.push(eq(courses.gradeLevel, grade as GradeLevel));
  }
  const subjectId = subject ? Number(subject) : undefined;
  if (subjectId) {
    filters.push(eq(courses.subjectId, subjectId));
  }
  filters.push(eq(courses.published, true));

  const rows = await db
    .select({
      id: courses.id,
      title: courses.title,
      slug: courses.slug,
      description: courses.description,
      gradeLevel: courses.gradeLevel,
      subjectName: subjects.name,
    })
    .from(courses)
    .innerJoin(subjects, eq(courses.subjectId, subjects.id))
    .where(and(...filters))
    .orderBy(courses.gradeLevel);

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl font-bold">Course catalog</h1>

      <form className="card flex flex-wrap items-end gap-4" method="get">
        <div className="flex flex-col gap-1">
          <label htmlFor="grade" className="text-sm font-medium">
            Grade
          </label>
          <select id="grade" name="grade" defaultValue={grade ?? ""} className="input">
            <option value="">All grades</option>
            {GRADE_LEVELS.map((g) => (
              <option key={g} value={g}>
                {gradeLabel(g)}
              </option>
            ))}
          </select>
        </div>
        <div className="flex flex-col gap-1">
          <label htmlFor="subject" className="text-sm font-medium">
            Subject
          </label>
          <select id="subject" name="subject" defaultValue={subject ?? ""} className="input">
            <option value="">All subjects</option>
            {allSubjects.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </div>
        <button type="submit" className="btn btn-primary">
          Filter
        </button>
      </form>

      {rows.length === 0 ? (
        <p className="text-black/60">No courses match those filters yet.</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {rows.map((course) => (
            <Link
              key={course.id}
              href={`/courses/${course.slug}`}
              className="card flex flex-col gap-2 transition hover:border-[--color-brand]"
            >
              <span className="w-fit rounded-full bg-[--color-brand-light] px-2 py-0.5 text-xs font-medium text-[--color-brand]">
                {gradeLabel(course.gradeLevel as GradeLevel)} · {course.subjectName}
              </span>
              <h2 className="font-semibold">{course.title}</h2>
              <p className="text-sm text-black/60">{course.description}</p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
