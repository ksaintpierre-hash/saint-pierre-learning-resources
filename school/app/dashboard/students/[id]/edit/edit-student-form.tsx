"use client";

import { useActionState } from "react";
import { editStudent, type EditStudentState } from "./actions";
import { GRADE_LEVELS, gradeLabel, type GradeLevel } from "@/lib/grades";
import { SupportNeedsFields } from "@/components/support-needs-fields";

const initialState: EditStudentState = {};

export function EditStudentForm({
  student,
}: {
  student: {
    id: number;
    name: string;
    gradeLevel: GradeLevel;
    aigIdentified: boolean;
    has504Plan: boolean;
    hasEcIep: boolean;
    isEnglishLearner: boolean;
    extendedTime: boolean;
    accommodationNotes: string;
  };
}) {
  const [state, formAction, pending] = useActionState(editStudent, initialState);

  return (
    <form action={formAction} className="card flex max-w-md flex-col gap-4">
      <input type="hidden" name="studentId" value={student.id} />
      <div className="flex flex-col gap-1">
        <label htmlFor="name" className="text-sm font-medium">
          Student name
        </label>
        <input id="name" name="name" className="input" required defaultValue={student.name} />
      </div>
      <div className="flex flex-col gap-1">
        <label htmlFor="gradeLevel" className="text-sm font-medium">
          Grade level
        </label>
        <select id="gradeLevel" name="gradeLevel" className="input" required defaultValue={student.gradeLevel}>
          {GRADE_LEVELS.map((g) => (
            <option key={g} value={g}>
              {gradeLabel(g)}
            </option>
          ))}
        </select>
      </div>
      <SupportNeedsFields defaults={student} />
      {state.error && <p className="text-sm text-red-600">{state.error}</p>}
      <button type="submit" className="btn btn-primary" disabled={pending}>
        {pending ? "Saving…" : "Save changes"}
      </button>
    </form>
  );
}
