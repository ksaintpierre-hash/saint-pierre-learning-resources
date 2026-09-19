"use client";

import { useActionState } from "react";
import { enrollStudent, type EnrollState } from "./actions";

const initialState: EnrollState = {};

export function EnrollForm({
  courseId,
  courseSlug,
  students,
}: {
  courseId: number;
  courseSlug: string;
  students: { id: number; name: string; alreadyEnrolled: boolean }[];
}) {
  const [state, formAction, pending] = useActionState(enrollStudent, initialState);

  const availableStudents = students.filter((s) => !s.alreadyEnrolled);

  if (students.length === 0) {
    return (
      <p className="text-sm text-black/60">
        Add a student profile from your dashboard before enrolling in a course.
      </p>
    );
  }

  if (availableStudents.length === 0) {
    return (
      <p className="text-sm text-[--color-brand]">
        {state.success ? "Enrolled! " : ""}All of your students are enrolled in this course.
      </p>
    );
  }

  return (
    <form action={formAction} className="flex flex-wrap items-end gap-3">
      <input type="hidden" name="courseId" value={courseId} />
      <input type="hidden" name="courseSlug" value={courseSlug} />
      <div className="flex flex-col gap-1">
        <label htmlFor="studentId" className="text-sm font-medium">
          Enroll student
        </label>
        <select id="studentId" name="studentId" className="input" required>
          {availableStudents.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
      </div>
      <button type="submit" className="btn btn-primary" disabled={pending}>
        {pending ? "Enrolling…" : "Enroll"}
      </button>
      {state.error && <p className="text-sm text-red-600">{state.error}</p>}
      {state.success && <p className="text-sm text-[--color-brand]">Enrolled!</p>}
    </form>
  );
}
