"use server";

import { z } from "zod";
import { redirect } from "next/navigation";
import { db } from "@/db";
import { students, GRADE_LEVELS } from "@/db/schema";
import { getSession } from "@/lib/session";

const schema = z.object({
  name: z.string().min(1, "Name is required."),
  gradeLevel: z.enum(GRADE_LEVELS),
});

export type AddStudentState = { error?: string };

export async function addStudent(_prevState: AddStudentState, formData: FormData): Promise<AddStudentState> {
  const session = await getSession();
  if (!session) {
    return { error: "You must be logged in." };
  }

  const parsed = schema.safeParse({
    name: formData.get("name"),
    gradeLevel: formData.get("gradeLevel"),
  });
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Invalid input." };
  }

  await db.insert(students).values({
    parentId: session.userId,
    name: parsed.data.name,
    gradeLevel: parsed.data.gradeLevel,
  });

  redirect("/dashboard");
}
