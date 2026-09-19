import Link from "next/link";
import { eq, and, count } from "drizzle-orm";
import { db } from "@/db";
import { students, enrollments, courses, lessons, lessonProgress } from "@/db/schema";
import { gradeLabel, type GradeLevel } from "@/lib/grades";
import { getSession } from "@/lib/session";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await getSession();
  if (!session) redirect("/login?next=/dashboard");

  const myStudents = await db
    .select()
    .from(students)
    .where(eq(students.parentId, session.userId));

  const studentSummaries = await Promise.all(
    myStudents.map(async (student) => {
      const studentEnrollments = await db
        .select({
          courseId: courses.id,
          title: courses.title,
          slug: courses.slug,
          gradeLevel: courses.gradeLevel,
        })
        .from(enrollments)
        .innerJoin(courses, eq(enrollments.courseId, courses.id))
        .where(eq(enrollments.studentId, student.id));

      const courseProgress = await Promise.all(
        studentEnrollments.map(async (enrollment) => {
          const [totalRow] = await db
            .select({ value: count() })
            .from(lessons)
            .where(eq(lessons.courseId, enrollment.courseId));

          const [doneRow] = await db
            .select({ value: count() })
            .from(lessonProgress)
            .innerJoin(lessons, eq(lessonProgress.lessonId, lessons.id))
            .where(and(eq(lessonProgress.studentId, student.id), eq(lessons.courseId, enrollment.courseId)));

          return {
            ...enrollment,
            total: totalRow?.value ?? 0,
            completed: doneRow?.value ?? 0,
          };
        }),
      );

      return { student, courseProgress };
    }),
  );

  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Your dashboard</h1>
        <Link href="/dashboard/students/new" className="btn btn-primary">
          Add a student
        </Link>
      </div>

      {studentSummaries.length === 0 && (
        <p className="text-black/60">
          You haven&apos;t added any students yet.{" "}
          <Link href="/dashboard/students/new" className="font-medium text-[--color-brand] underline">
            Add your first student
          </Link>{" "}
          to start enrolling in courses.
        </p>
      )}

      {studentSummaries.map(({ student, courseProgress }) => (
        <section key={student.id} className="card flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">{student.name}</h2>
            <span className="text-sm text-black/60">{gradeLabel(student.gradeLevel as GradeLevel)}</span>
          </div>

          {courseProgress.length === 0 ? (
            <p className="text-sm text-black/60">
              Not enrolled in any courses yet.{" "}
              <Link href="/courses" className="font-medium text-[--color-brand] underline">
                Browse the catalog
              </Link>
              .
            </p>
          ) : (
            <ul className="flex flex-col gap-2">
              {courseProgress.map((c) => (
                <li key={c.courseId} className="flex items-center justify-between border-t border-black/5 pt-2 first:border-0 first:pt-0">
                  <Link href={`/courses/${c.slug}`} className="font-medium text-[--color-brand] underline">
                    {c.title}
                  </Link>
                  <span className="text-sm text-black/60">
                    {c.completed}/{c.total} lessons complete
                  </span>
                </li>
              ))}
            </ul>
          )}
        </section>
      ))}
    </div>
  );
}
