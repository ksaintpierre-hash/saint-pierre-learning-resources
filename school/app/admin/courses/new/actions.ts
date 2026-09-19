"use server";

import { z } from "zod";
import { redirect } from "next/navigation";
import { db } from "@/db";
import { courses, GRADE_LEVELS } from "@/db/schema";
import { getSession } from "@/lib/session";

const schema = z.object({
  title: z.string().min(1, "Title is required."),
  description: z.string().min(1, "Description is required."),
  gradeLevel: z.enum(GRADE_LEVELS),
  subjectId: z.coerce.number().int().positive(),
});

function slugify(title: string) {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

export type NewCourseState = { error?: string };

export async function createCourse(_prevState: NewCourseState, formData: FormData): Promise<NewCourseState> {
  const session = await getSession();
  if (session?.role !== "admin") {
    return { error: "Only admins can create courses." };
  }

  const parsed = schema.safeParse({
    title: formData.get("title"),
    description: formData.get("description"),
    gradeLevel: formData.get("gradeLevel"),
    subjectId: formData.get("subjectId"),
  });
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Invalid input." };
  }

  const { title, description, gradeLevel, subjectId } = parsed.data;
  const slug = `${slugify(title)}-${gradeLevel.toLowerCase()}`;

  const [course] = await db
    .insert(courses)
    .values({ title, description, gradeLevel, subjectId, slug })
    .returning();

  redirect(`/admin/courses/${course.id}/lessons/new`);
}
