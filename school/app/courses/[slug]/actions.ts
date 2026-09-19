"use server";

import { z } from "zod";
import { eq, and } from "drizzle-orm";
import { revalidatePath } from "next/cache";
import { db } from "@/db";
import { enrollments, students } from "@/db/schema";
import { getSession } from "@/lib/session";

const schema = z.object({
  studentId: z.coerce.number().int().positive(),
  courseId: z.coerce.number().int().positive(),
  courseSlug: z.string().min(1),
});

export type EnrollState = { error?: string; success?: boolean };

export async function enrollStudent(_prevState: EnrollState, formData: FormData): Promise<EnrollState> {
  const session = await getSession();
  if (!session) {
    return { error: "You must be logged in to enroll a student." };
  }

  const parsed = schema.safeParse({
    studentId: formData.get("studentId"),
    courseId: formData.get("courseId"),
    courseSlug: formData.get("courseSlug"),
  });
  if (!parsed.success) {
    return { error: "Invalid enrollment request." };
  }
  const { studentId, courseId, courseSlug } = parsed.data;

  const [student] = await db
    .select()
    .from(students)
    .where(and(eq(students.id, studentId), eq(students.parentId, session.userId)))
    .limit(1);
  if (!student) {
    return { error: "That student profile was not found." };
  }

  const [existing] = await db
    .select()
    .from(enrollments)
    .where(and(eq(enrollments.studentId, studentId), eq(enrollments.courseId, courseId)))
    .limit(1);

  if (!existing) {
    await db.insert(enrollments).values({ studentId, courseId });
  }

  revalidatePath(`/courses/${courseSlug}`);
  return { success: true };
}
