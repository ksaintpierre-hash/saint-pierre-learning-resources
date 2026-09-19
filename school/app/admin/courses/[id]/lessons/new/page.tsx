import { eq } from "drizzle-orm";
import { notFound } from "next/navigation";
import { db } from "@/db";
import { courses, lessons } from "@/db/schema";
import { NewLessonForm } from "./new-lesson-form";

export default async function NewLessonPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const courseId = Number(id);
  if (!Number.isInteger(courseId)) notFound();

  const [course] = await db.select().from(courses).where(eq(courses.id, courseId)).limit(1);
  if (!course) notFound();

  const existingLessons = await db
    .select()
    .from(lessons)
    .where(eq(lessons.courseId, courseId))
    .orderBy(lessons.sortOrder);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold">Add a lesson</h1>
        <p className="text-black/60">{course.title}</p>
      </div>

      {existingLessons.length > 0 && (
        <ol className="flex flex-col gap-2">
          {existingLessons.map((lesson, index) => (
            <li key={lesson.id} className="card">
              <span className="mr-2 text-black/40">{index + 1}.</span>
              {lesson.title}
            </li>
          ))}
        </ol>
      )}

      <NewLessonForm courseId={course.id} />
    </div>
  );
}
