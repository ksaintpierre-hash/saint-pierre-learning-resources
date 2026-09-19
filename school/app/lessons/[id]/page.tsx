import Link from "next/link";
import { notFound } from "next/navigation";
import { eq, and, inArray } from "drizzle-orm";
import { db } from "@/db";
import { lessons, courses, students, enrollments, lessonProgress } from "@/db/schema";
import { getSession } from "@/lib/session";
import { CompleteForm } from "./complete-form";

export default async function LessonPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const lessonId = Number(id);
  if (!Number.isInteger(lessonId)) notFound();

  const [lesson] = await db.select().from(lessons).where(eq(lessons.id, lessonId)).limit(1);
  if (!lesson) notFound();

  const [course] = await db.select().from(courses).where(eq(courses.id, lesson.courseId)).limit(1);

  const session = await getSession();
  let enrolledStudents: { id: number; name: string; completed: boolean }[] = [];

  if (session?.role === "parent") {
    const parentStudents = await db
      .select()
      .from(students)
      .where(eq(students.parentId, session.userId));
    const studentIds = parentStudents.map((s) => s.id);

    const relevantEnrollments =
      studentIds.length > 0
        ? await db
            .select()
            .from(enrollments)
            .where(and(eq(enrollments.courseId, lesson.courseId), inArray(enrollments.studentId, studentIds)))
        : [];
    const enrolledIds = new Set(relevantEnrollments.map((e) => e.studentId));

    const completions =
      enrolledIds.size > 0
        ? await db
            .select()
            .from(lessonProgress)
            .where(and(eq(lessonProgress.lessonId, lessonId), inArray(lessonProgress.studentId, [...enrolledIds])))
        : [];
    const completedIds = new Set(completions.map((c) => c.studentId));

    enrolledStudents = parentStudents
      .filter((s) => enrolledIds.has(s.id))
      .map((s) => ({ id: s.id, name: s.name, completed: completedIds.has(s.id) }));
  }

  return (
    <div className="flex flex-col gap-6">
      {course && (
        <Link href={`/courses/${course.slug}`} className="text-sm font-medium text-[--color-brand] underline">
          ← Back to {course.title}
        </Link>
      )}

      <h1 className="text-2xl font-bold">{lesson.title}</h1>

      {lesson.contentType === "video" && lesson.videoUrl && (
        <div className="card">
          <p className="text-sm text-black/60">Video lesson</p>
          <a href={lesson.videoUrl} target="_blank" rel="noreferrer" className="font-medium text-[--color-brand] underline">
            {lesson.videoUrl}
          </a>
        </div>
      )}

      <div className="card prose max-w-none whitespace-pre-wrap">{lesson.contentBody}</div>

      <div className="card">
        <h2 className="mb-3 font-semibold">Progress</h2>
        {session?.role === "parent" ? (
          <CompleteForm lessonId={lesson.id} students={enrolledStudents} />
        ) : (
          <p className="text-sm text-black/60">
            <Link href={`/login?next=/lessons/${lesson.id}`} className="font-medium text-[--color-brand] underline">
              Log in
            </Link>{" "}
            as a parent to track lesson completion for your students.
          </p>
        )}
      </div>
    </div>
  );
}
