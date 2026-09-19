import { db } from "@/db";
import { subjects } from "@/db/schema";
import { NewCourseForm } from "./new-course-form";

export default async function NewCoursePage() {
  const allSubjects = await db.select().from(subjects).orderBy(subjects.name);

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl font-bold">New course</h1>
      <NewCourseForm subjects={allSubjects} />
    </div>
  );
}
