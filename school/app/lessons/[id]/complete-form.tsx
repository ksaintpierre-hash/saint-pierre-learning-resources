"use client";

import { useActionState } from "react";
import { markLessonComplete, type ProgressState } from "./actions";

const initialState: ProgressState = {};

export function CompleteForm({
  lessonId,
  students,
}: {
  lessonId: number;
  students: { id: number; name: string; completed: boolean }[];
}) {
  const [state, formAction, pending] = useActionState(markLessonComplete, initialState);

  const pendingStudents = students.filter((s) => !s.completed);

  if (students.length === 0) {
    return (
      <p className="text-sm text-black/60">
        No enrolled students yet. Enroll a student in this course to track lesson progress.
      </p>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      {students
        .filter((s) => s.completed)
        .map((s) => (
          <p key={s.id} className="text-sm text-[--color-brand]">
            ✓ {s.name} completed this lesson.
          </p>
        ))}

      {pendingStudents.length > 0 && (
        <form action={formAction} className="flex flex-wrap items-end gap-3">
          <input type="hidden" name="lessonId" value={lessonId} />
          <div className="flex flex-col gap-1">
            <label htmlFor="studentId" className="text-sm font-medium">
              Mark complete for
            </label>
            <select id="studentId" name="studentId" className="input" required>
              {pendingStudents.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
          </div>
          <button type="submit" className="btn btn-primary" disabled={pending}>
            {pending ? "Saving…" : "Mark complete"}
          </button>
        </form>
      )}
      {state.error && <p className="text-sm text-red-600">{state.error}</p>}
    </div>
  );
}
