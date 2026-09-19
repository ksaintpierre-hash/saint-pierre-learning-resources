import { db } from "../db";
import { users, subjects, courses, lessons } from "../db/schema";
import { hashPassword } from "../lib/auth";
import { eq } from "drizzle-orm";

async function upsertSubject(name: string, slug: string) {
  const [existing] = await db.select().from(subjects).where(eq(subjects.slug, slug)).limit(1);
  if (existing) return existing;
  const [created] = await db.insert(subjects).values({ name, slug }).returning();
  return created;
}

async function upsertCourse(input: {
  title: string;
  slug: string;
  description: string;
  gradeLevel: (typeof import("../db/schema").GRADE_LEVELS)[number];
  subjectId: number;
  lessons: { title: string; contentBody: string }[];
}) {
  const [existing] = await db.select().from(courses).where(eq(courses.slug, input.slug)).limit(1);
  if (existing) return existing;

  const [course] = await db
    .insert(courses)
    .values({
      title: input.title,
      slug: input.slug,
      description: input.description,
      gradeLevel: input.gradeLevel,
      subjectId: input.subjectId,
    })
    .returning();

  for (const [index, lesson] of input.lessons.entries()) {
    await db.insert(lessons).values({
      courseId: course.id,
      title: lesson.title,
      sortOrder: index,
      contentType: "text",
      contentBody: lesson.contentBody,
    });
  }

  return course;
}

async function main() {
  const adminEmail = "admin@saintpierrecharles.school";
  const [existingAdmin] = await db.select().from(users).where(eq(users.email, adminEmail)).limit(1);
  if (!existingAdmin) {
    await db.insert(users).values({
      email: adminEmail,
      name: "School Admin",
      role: "admin",
      passwordHash: await hashPassword("ChangeMe123!"),
    });
    console.log(`Created admin user: ${adminEmail} / ChangeMe123!`);
  }

  const ela = await upsertSubject("English Language Arts", "ela");
  const math = await upsertSubject("Math", "math");

  await upsertCourse({
    title: "Letters and Sounds",
    slug: "letters-and-sounds-pk",
    description: "Introducing letter recognition and beginning sounds for our youngest learners.",
    gradeLevel: "PK",
    subjectId: ela.id,
    lessons: [
      { title: "Meet the alphabet", contentBody: "Sing the alphabet song and point to each letter as you go." },
      { title: "Beginning sounds: A, B, C", contentBody: "Practice the sounds each letter makes with picture cards." },
    ],
  });

  await upsertCourse({
    title: "Counting to 10",
    slug: "counting-to-10-pk",
    description: "Hands-on counting practice from 1 to 10.",
    gradeLevel: "PK",
    subjectId: math.id,
    lessons: [
      { title: "Counting objects 1-5", contentBody: "Count everyday objects around the house, from one to five." },
      { title: "Counting objects 6-10", contentBody: "Continue counting practice up through ten." },
    ],
  });

  await upsertCourse({
    title: "Sight Words and Early Reading",
    slug: "sight-words-early-reading-k",
    description: "Building a foundation of common sight words and simple sentences.",
    gradeLevel: "K",
    subjectId: ela.id,
    lessons: [
      { title: "First 10 sight words", contentBody: "Read and practice: the, a, I, is, you, to, and, we, my, see." },
      { title: "Reading simple sentences", contentBody: "Put sight words together into short, decodable sentences." },
    ],
  });

  await upsertCourse({
    title: "Story Elements",
    slug: "story-elements-grade-1",
    description: "Identifying characters, setting, and plot in short stories.",
    gradeLevel: "1",
    subjectId: ela.id,
    lessons: [
      { title: "Who and where: characters and setting", contentBody: "Read a short story and identify who is in it and where it happens." },
      { title: "What happens: plot", contentBody: "Sequence the beginning, middle, and end of a story." },
    ],
  });

  await upsertCourse({
    title: "Addition and Subtraction Within 20",
    slug: "addition-subtraction-20-grade-1",
    description: "Building fluency with addition and subtraction facts.",
    gradeLevel: "1",
    subjectId: math.id,
    lessons: [
      { title: "Addition facts to 20", contentBody: "Practice addition facts using number lines and manipulatives." },
      { title: "Subtraction facts to 20", contentBody: "Practice subtraction facts using number lines and manipulatives." },
    ],
  });

  await upsertCourse({
    title: "Multiplication Foundations",
    slug: "multiplication-foundations-grade-3",
    description: "Understanding multiplication as repeated addition and equal groups.",
    gradeLevel: "3",
    subjectId: math.id,
    lessons: [
      { title: "Equal groups and arrays", contentBody: "Model multiplication using equal groups and arrays." },
      { title: "Multiplication facts 0-5", contentBody: "Practice multiplication facts for factors 0 through 5." },
    ],
  });

  await upsertCourse({
    title: "Evidence in Informational Text",
    slug: "ri-7-1-evidence-in-informational-text",
    description: "Citing strong textual evidence to support analysis of informational text.",
    gradeLevel: "7",
    subjectId: ela.id,
    lessons: [
      { title: "Explicit vs. inferred evidence", contentBody: "Distinguish between what a text says directly and what it implies." },
      { title: "Citing evidence in writing", contentBody: "Practice quoting and paraphrasing evidence to support a claim." },
    ],
  });

  await upsertCourse({
    title: "Linear Equations",
    slug: "linear-equations-grade-10",
    description: "Solving and graphing linear equations in one and two variables.",
    gradeLevel: "10",
    subjectId: math.id,
    lessons: [
      { title: "Solving one-variable equations", contentBody: "Practice isolating the variable using inverse operations." },
      { title: "Graphing lines from slope-intercept form", contentBody: "Plot lines given an equation in y = mx + b form." },
    ],
  });

  console.log("Seed complete.");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
