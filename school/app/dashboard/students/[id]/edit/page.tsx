import { eq, and } from "drizzle-orm";
import { notFound, redirect } from "next/navigation";
import { db } from "@/db";
import { students } from "@/db/schema";
import { getSession } from "@/lib/session";
import { EditStudentForm } from "./edit-student-form";

export default async function EditStudentPage({ params }: { params: Promise<{ id: string }> }) {
  const session = await getSession();
  if (!session) redirect("/login?next=/dashboard");

  const { id } = await params;
  const studentId = Number(id);
  if (!Number.isInteger(studentId)) notFound();

  const [student] = await db
    .select()
    .from(students)
    .where(and(eq(students.id, studentId), eq(students.parentId, session.userId)))
    .limit(1);
  if (!student) notFound();

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl font-bold">Edit {student.name}</h1>
      <EditStudentForm student={student} />
    </div>
  );
}
