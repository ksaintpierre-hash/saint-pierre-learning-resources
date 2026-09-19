import { GRADE_LEVELS, type GradeLevel } from "@/db/schema";

export { GRADE_LEVELS };
export type { GradeLevel };

export function gradeLabel(grade: GradeLevel): string {
  if (grade === "PK") return "Pre-K";
  if (grade === "K") return "Kindergarten";
  return `Grade ${grade}`;
}
