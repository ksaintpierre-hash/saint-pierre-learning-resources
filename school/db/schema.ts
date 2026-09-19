import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";
import { sql } from "drizzle-orm";

// Ordered grade bands from Pre-K through 12th grade.
export const GRADE_LEVELS = [
  "PK",
  "K",
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "10",
  "11",
  "12",
] as const;

export type GradeLevel = (typeof GRADE_LEVELS)[number];

export const users = sqliteTable("users", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  email: text("email").notNull().unique(),
  passwordHash: text("password_hash").notNull(),
  name: text("name").notNull(),
  role: text("role", { enum: ["parent", "admin"] })
    .notNull()
    .default("parent"),
  createdAt: text("created_at")
    .notNull()
    .default(sql`(current_timestamp)`),
});

export const students = sqliteTable("students", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  parentId: integer("parent_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  name: text("name").notNull(),
  gradeLevel: text("grade_level", { enum: GRADE_LEVELS }).notNull(),
  createdAt: text("created_at")
    .notNull()
    .default(sql`(current_timestamp)`),
});

export const subjects = sqliteTable("subjects", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  name: text("name").notNull(),
  slug: text("slug").notNull().unique(),
});

export const courses = sqliteTable("courses", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  title: text("title").notNull(),
  slug: text("slug").notNull().unique(),
  description: text("description").notNull(),
  gradeLevel: text("grade_level", { enum: GRADE_LEVELS }).notNull(),
  subjectId: integer("subject_id")
    .notNull()
    .references(() => subjects.id, { onDelete: "cascade" }),
  priceCents: integer("price_cents").notNull().default(999),
  published: integer("published", { mode: "boolean" }).notNull().default(true),
  createdAt: text("created_at")
    .notNull()
    .default(sql`(current_timestamp)`),
});

export const lessons = sqliteTable("lessons", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  courseId: integer("course_id")
    .notNull()
    .references(() => courses.id, { onDelete: "cascade" }),
  title: text("title").notNull(),
  sortOrder: integer("sort_order").notNull().default(0),
  contentType: text("content_type", { enum: ["text", "video", "worksheet"] })
    .notNull()
    .default("text"),
  contentBody: text("content_body").notNull().default(""),
  videoUrl: text("video_url"),
});

export const enrollments = sqliteTable("enrollments", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  studentId: integer("student_id")
    .notNull()
    .references(() => students.id, { onDelete: "cascade" }),
  courseId: integer("course_id")
    .notNull()
    .references(() => courses.id, { onDelete: "cascade" }),
  enrolledAt: text("enrolled_at")
    .notNull()
    .default(sql`(current_timestamp)`),
});

export const lessonProgress = sqliteTable("lesson_progress", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  studentId: integer("student_id")
    .notNull()
    .references(() => students.id, { onDelete: "cascade" }),
  lessonId: integer("lesson_id")
    .notNull()
    .references(() => lessons.id, { onDelete: "cascade" }),
  completedAt: text("completed_at")
    .notNull()
    .default(sql`(current_timestamp)`),
});
