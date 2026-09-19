import Link from "next/link";
import { eq } from "drizzle-orm";
import { db } from "@/db";
import { courses, subjects } from "@/db/schema";
import { gradeLabel, type GradeLevel } from "@/lib/grades";
import { formatPrice } from "@/lib/money";

export default async function AdminPage() {
  const rows = await db
    .select({
      id: courses.id,
      title: courses.title,
      slug: courses.slug,
      gradeLevel: courses.gradeLevel,
      priceCents: courses.priceCents,
      published: courses.published,
      subjectName: subjects.name,
    })
    .from(courses)
    .innerJoin(subjects, eq(courses.subjectId, subjects.id))
    .orderBy(courses.gradeLevel);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Manage courses</h1>
        <Link href="/admin/courses/new" className="btn btn-primary">
          New course
        </Link>
      </div>

      <div className="flex flex-col gap-2">
        {rows.map((course) => (
          <div key={course.id} className="card flex items-center justify-between">
            <div>
              <p className="font-medium">{course.title}</p>
              <p className="text-sm text-black/60">
                {gradeLabel(course.gradeLevel as GradeLevel)} · {course.subjectName} ·{" "}
                {formatPrice(course.priceCents)}
                {!course.published && " · Draft"}
              </p>
            </div>
            <div className="flex gap-3 text-sm font-medium">
              <Link href={`/admin/courses/${course.id}/lessons/new`} className="text-[--color-brand] underline">
                Add lesson
              </Link>
              <Link href={`/courses/${course.slug}`} className="text-[--color-brand] underline">
                View
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
