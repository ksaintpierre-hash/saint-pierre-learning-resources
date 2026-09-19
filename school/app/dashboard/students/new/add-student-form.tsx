"use client";

import { useActionState } from "react";
import { addStudent, type AddStudentState } from "./actions";
import { GRADE_LEVELS, gradeLabel } from "@/lib/grades";

const initialState: AddStudentState = {};

export function AddStudentForm() {
  const [state, formAction, pending] = useActionState(addStudent, initialState);

  return (
    <form action={formAction} className="card flex max-w-md flex-col gap-4">
      <div className="flex flex-col gap-1">
        <label htmlFor="name" className="text-sm font-medium">
          Student name
        </label>
        <input id="name" name="name" className="input" required />
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
      {state.error && <p className="text-sm text-red-600">{state.error}</p>}
      <button type="submit" className="btn btn-primary" disabled={pending}>
        {pending ? "Adding…" : "Add student"}
      </button>
    </form>
  );
}
