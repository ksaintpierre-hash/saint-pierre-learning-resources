import Link from "next/link";
import { SignupForm } from "./signup-form";

export default function SignupPage() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold">Create your parent account</h1>
        <p className="text-sm text-black/60">
          Already have an account?{" "}
          <Link href="/login" className="font-medium text-[--color-brand] underline">
            Log in
          </Link>
        </p>
      </div>
      <SignupForm />
    </div>
  );
}
