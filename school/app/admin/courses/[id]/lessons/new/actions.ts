"use server";

import { z } from "zod";
import { eq, count } from "drizzle-orm";
import { revalidatePath } from "next/cache";
import { db } from "@/db";
import { lessons } from "@/db/schema";
import { getSession } from "@/lib/session";

const schema = z.object({
  courseId: z.coerce.number().int().positive(),
  title: z.string().min(1, "Title is required."),
  contentType: z.enum(["text", "video", "worksheet"]),
  contentBody: z.string().min(1, "Lesson content is required."),
  videoUrl: z.string().optional(),
});

export type NewLessonState = { error?: string; success?: boolean };

export async function createLesson(_prevState: NewLessonState, formData: FormData): Promise<NewLessonState> {
  const session = await getSession();
  if (session?.role !== "admin") {
    return { error: "Only admins can add lessons." };
  }

  const parsed = schema.safeParse({
    courseId: formData.get("courseId"),
    title: formData.get("title"),
    contentType: formData.get("contentType"),
    contentBody: formData.get("contentBody"),
    videoUrl: formData.get("videoUrl") || undefined,
  });
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Invalid input." };
  }

  const { courseId, title, contentType, contentBody, videoUrl } = parsed.data;

  const [{ value: existingCount }] = await db
    .select({ value: count() })
    .from(lessons)
    .where(eq(lessons.courseId, courseId));

  await db.insert(lessons).values({
    courseId,
    title,
    contentType,
    contentBody,
    videoUrl: videoUrl ?? null,
    sortOrder: existingCount,
  });

  revalidatePath(`/admin/courses/${courseId}/lessons/new`);
  return { success: true };
}
