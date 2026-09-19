import Link from "next/link";
import { notFound } from "next/navigation";
import { eq, and, inArray } from "drizzle-orm";
import { db } from "@/db";
import { courses, subjects, lessons, students, enrollments } from "@/db/schema";
import { gradeLabel, type GradeLevel } from "@/lib/grades";
import { formatPrice } from "@/lib/money";
import { getSession } from "@/lib/session";
import { EnrollForm } from "./enroll-form";

export default async function CourseDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;

  const [course] = await db
    .select({
      id: courses.id,
      title: courses.title,
      slug: courses.slug,
      description: courses.description,
      gradeLevel: courses.gradeLevel,
      priceCents: courses.priceCents,
      subjectName: subjects.name,
    })
    .from(courses)
    .innerJoin(subjects, eq(courses.subjectId, subjects.id))
    .where(eq(courses.slug, slug))
    .limit(1);

  if (!course) notFound();

  const courseLessons = await db
    .select()
    .from(lessons)
    .where(eq(lessons.courseId, course.id))
    .orderBy(lessons.sortOrder);

  const session = await getSession();
  let myStudents: { id: number; name: string; alreadyEnrolled: boolean }[] = [];

  if (session?.role === "parent") {
    const parentStudents = await db
      .select()
      .from(students)
      .where(eq(students.parentId, session.userId));

    const studentIds = parentStudents.map((s) => s.id);
    const existingEnrollments =
      studentIds.length > 0
        ? await db
            .select()
            .from(enrollments)
            .where(and(eq(enrollments.courseId, course.id), inArray(enrollments.studentId, studentIds)))
        : [];
    const enrolledIds = new Set(existingEnrollments.map((e) => e.studentId));

    myStudents = parentStudents.map((s) => ({
      id: s.id,
      name: s.name,
      alreadyEnrolled: enrolledIds.has(s.id),
    }));
  }

  return (
    <div className="flex flex-col gap-8">
      <div>
        <span className="w-fit rounded-full bg-[--color-brand-light] px-2 py-0.5 text-xs font-medium text-[--color-brand]">
          {gradeLabel(course.gradeLevel as GradeLevel)} · {course.subjectName}
        </span>
        <h1 className="mt-2 text-3xl font-bold">{course.title}</h1>
        <p className="mt-2 text-black/70">{course.description}</p>
        <p className="mt-2 text-lg font-semibold text-[--color-brand]">{formatPrice(course.priceCents)}</p>
      </div>

      <div className="card">
        {session?.role === "parent" ? (
          <EnrollForm courseId={course.id} courseSlug={course.slug} students={myStudents} />
        ) : session?.role === "admin" ? (
          <p className="text-sm text-black/60">Admin accounts can&apos;t enroll students.</p>
        ) : (
          <p className="text-sm text-black/60">
            <Link href={`/login?next=/courses/${course.slug}`} className="font-medium text-[--color-brand] underline">
              Log in
            </Link>{" "}
            or{" "}
            <Link href="/signup" className="font-medium text-[--color-brand] underline">
              create a parent account
            </Link>{" "}
            to enroll a student in this course.
          </p>
        )}
      </div>

      <div>
        <h2 className="text-xl font-semibold">Lessons</h2>
        <ol className="mt-3 flex flex-col gap-2">
          {courseLessons.map((lesson, index) => (
            <li key={lesson.id} className="card flex items-center justify-between">
              <span>
                <span className="mr-2 text-black/40">{index + 1}.</span>
                {lesson.title}
              </span>
              <Link href={`/lessons/${lesson.id}`} className="text-sm font-medium text-[--color-brand] underline">
                View lesson
              </Link>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
