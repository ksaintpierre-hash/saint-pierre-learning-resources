import Link from "next/link";
import { LoginForm } from "./login-form";

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string }>;
}) {
  const { next } = await searchParams;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold">Log in</h1>
        <p className="text-sm text-black/60">
          Need an account?{" "}
          <Link href="/signup" className="font-medium text-[--color-brand] underline">
            Sign up
          </Link>
        </p>
      </div>
      <LoginForm next={next} />
    </div>
  );
}
