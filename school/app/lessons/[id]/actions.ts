"use server";

import { z } from "zod";
import { eq, and } from "drizzle-orm";
import { revalidatePath } from "next/cache";
import { db } from "@/db";
import { lessonProgress, students } from "@/db/schema";
import { getSession } from "@/lib/session";

const schema = z.object({
  studentId: z.coerce.number().int().positive(),
  lessonId: z.coerce.number().int().positive(),
});

export type ProgressState = { error?: string; success?: boolean };

export async function markLessonComplete(
  _prevState: ProgressState,
  formData: FormData,
): Promise<ProgressState> {
  const session = await getSession();
  if (!session) {
    return { error: "You must be logged in." };
  }

  const parsed = schema.safeParse({
    studentId: formData.get("studentId"),
    lessonId: formData.get("lessonId"),
  });
  if (!parsed.success) {
    return { error: "Invalid request." };
  }
  const { studentId, lessonId } = parsed.data;

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
    .from(lessonProgress)
    .where(and(eq(lessonProgress.studentId, studentId), eq(lessonProgress.lessonId, lessonId)))
    .limit(1);

  if (!existing) {
    await db.insert(lessonProgress).values({ studentId, lessonId });
  }

  revalidatePath(`/lessons/${lessonId}`);
  return { success: true };
}
