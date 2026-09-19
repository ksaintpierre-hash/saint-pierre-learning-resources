"use client";

import { useActionState } from "react";
import { createCourse, type NewCourseState } from "./actions";
import { GRADE_LEVELS, gradeLabel } from "@/lib/grades";

const initialState: NewCourseState = {};

export function NewCourseForm({ subjects }: { subjects: { id: number; name: string }[] }) {
  const [state, formAction, pending] = useActionState(createCourse, initialState);

  return (
    <form action={formAction} className="card flex max-w-lg flex-col gap-4">
      <div className="flex flex-col gap-1">
        <label htmlFor="title" className="text-sm font-medium">
          Title
        </label>
        <input id="title" name="title" className="input" required />
      </div>
      <div className="flex flex-col gap-1">
        <label htmlFor="description" className="text-sm font-medium">
          Description
        </label>
        <textarea id="description" name="description" className="input" rows={3} required />
      </div>
      <div className="flex flex-col gap-1">
        <label htmlFor="gradeLevel" className="text-sm font-medium">
          Grade level
        </label>
        <select id="gradeLevel" name="gradeLevel" className="input" required defaultValue="">
          <option value="" disabled>
            Select a grade
          </option>
          {GRADE_LEVELS.map((g) => (
            <option key={g} value={g}>
              {gradeLabel(g)}
            </option>
          ))}
        </select>
      </div>
      <div className="flex flex-col gap-1">
        <label htmlFor="subjectId" className="text-sm font-medium">
          Subject
        </label>
        <select id="subjectId" name="subjectId" className="input" required defaultValue="">
          <option value="" disabled>
            Select a subject
          </option>
          {subjects.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
      </div>
      <div className="flex flex-col gap-1">
        <label htmlFor="price" className="text-sm font-medium">
          Price (USD)
        </label>
        <input
          id="price"
          name="price"
          type="number"
          step="0.01"
          min="0"
          className="input"
          required
          defaultValue="9.99"
        />
      </div>
      {state.error && <p className="text-sm text-red-600">{state.error}</p>}
      <button type="submit" className="btn btn-primary" disabled={pending}>
        {pending ? "Creating…" : "Create course"}
      </button>
    </form>
  );
}
