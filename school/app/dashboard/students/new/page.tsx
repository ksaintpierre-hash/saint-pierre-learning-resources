import { AddStudentForm } from "./add-student-form";

export default function NewStudentPage() {
  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl font-bold">Add a student</h1>
      <AddStudentForm />
    </div>
  );
}
