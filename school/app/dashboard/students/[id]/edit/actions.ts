"use server";

import { z } from "zod";
import { eq, and } from "drizzle-orm";
import { redirect } from "next/navigation";
import { db } from "@/db";
import { students, GRADE_LEVELS } from "@/db/schema";
import { getSession } from "@/lib/session";

const schema = z.object({
  studentId: z.coerce.number().int().positive(),
  name: z.string().min(1, "Name is required."),
  gradeLevel: z.enum(GRADE_LEVELS),
  aigIdentified: z.coerce.boolean(),
  has504Plan: z.coerce.boolean(),
  hasEcIep: z.coerce.boolean(),
  extendedTime: z.coerce.boolean(),
  accommodationNotes: z.string(),
});

export type EditStudentState = { error?: string };

export async function editStudent(_prevState: EditStudentState, formData: FormData): Promise<EditStudentState> {
  const session = await getSession();
  if (!session) {
    return { error: "You must be logged in." };
  }

  const parsed = schema.safeParse({
    studentId: formData.get("studentId"),
    name: formData.get("name"),
    gradeLevel: formData.get("gradeLevel"),
    aigIdentified: formData.get("aigIdentified") === "on",
    has504Plan: formData.get("has504Plan") === "on",
    hasEcIep: formData.get("hasEcIep") === "on",
    extendedTime: formData.get("extendedTime") === "on",
    accommodationNotes: formData.get("accommodationNotes") ?? "",
  });
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Invalid input." };
  }

  const { studentId, ...updates } = parsed.data;

  const [student] = await db
    .select()
    .from(students)
    .where(and(eq(students.id, studentId), eq(students.parentId, session.userId)))
    .limit(1);
  if (!student) {
    return { error: "That student profile was not found." };
  }

  await db.update(students).set(updates).where(eq(students.id, studentId));

  redirect("/dashboard");
}
