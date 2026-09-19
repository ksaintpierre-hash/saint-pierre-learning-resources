"use server";

import { z } from "zod";
import { redirect } from "next/navigation";
import { db } from "@/db";
import { students, GRADE_LEVELS } from "@/db/schema";
import { getSession } from "@/lib/session";

const schema = z.object({
  name: z.string().min(1, "Name is required."),
  gradeLevel: z.enum(GRADE_LEVELS),
  aigIdentified: z.coerce.boolean(),
  has504Plan: z.coerce.boolean(),
  hasEcIep: z.coerce.boolean(),
  isEnglishLearner: z.coerce.boolean(),
  extendedTime: z.coerce.boolean(),
  accommodationNotes: z.string(),
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
    aigIdentified: formData.get("aigIdentified") === "on",
    has504Plan: formData.get("has504Plan") === "on",
    hasEcIep: formData.get("hasEcIep") === "on",
    isEnglishLearner: formData.get("isEnglishLearner") === "on",
    extendedTime: formData.get("extendedTime") === "on",
    accommodationNotes: formData.get("accommodationNotes") ?? "",
  });
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Invalid input." };
  }

  await db.insert(students).values({
    parentId: session.userId,
    ...parsed.data,
  });

  redirect("/dashboard");
}
