"use client";

import { useActionState } from "react";
import { createLesson, type NewLessonState } from "./actions";

const initialState: NewLessonState = {};

export function NewLessonForm({ courseId }: { courseId: number }) {
  const [state, formAction, pending] = useActionState(createLesson, initialState);

  return (
    <form action={formAction} className="card flex max-w-lg flex-col gap-4">
      <input type="hidden" name="courseId" value={courseId} />
      <div className="flex flex-col gap-1">
        <label htmlFor="title" className="text-sm font-medium">
          Lesson title
        </label>
        <input id="title" name="title" className="input" required />
      </div>
      <div className="flex flex-col gap-1">
        <label htmlFor="contentType" className="text-sm font-medium">
          Content type
        </label>
        <select id="contentType" name="contentType" className="input" defaultValue="text">
          <option value="text">Text</option>
          <option value="video">Video</option>
          <option value="worksheet">Worksheet</option>
        </select>
      </div>
      <div className="flex flex-col gap-1">
        <label htmlFor="videoUrl" className="text-sm font-medium">
          Video URL (optional)
        </label>
        <input id="videoUrl" name="videoUrl" className="input" placeholder="https://…" />
      </div>
      <div className="flex flex-col gap-1">
        <label htmlFor="contentBody" className="text-sm font-medium">
          Lesson content
        </label>
        <textarea id="contentBody" name="contentBody" className="input" rows={8} required />
      </div>
      {state.error && <p className="text-sm text-red-600">{state.error}</p>}
      {state.success && <p className="text-sm text-[--color-brand]">Lesson added.</p>}
      <button type="submit" className="btn btn-primary" disabled={pending}>
        {pending ? "Saving…" : "Add lesson"}
      </button>
    </form>
  );
}
