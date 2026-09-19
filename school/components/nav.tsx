import Link from "next/link";
import { getSession } from "@/lib/session";

export async function Nav() {
  const session = await getSession();

  return (
    <header className="border-b border-black/10 bg-white">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
        <Link href="/" className="text-lg font-bold text-[--color-brand]">
          Saint Pierre-Charles Online School
        </Link>
        <nav className="flex items-center gap-4 text-sm font-medium">
          <Link href="/courses">Courses</Link>
          {session?.role === "admin" && <Link href="/admin">Admin</Link>}
          {session ? (
            <>
              <Link href="/dashboard">Dashboard</Link>
              <form action="/logout" method="post">
                <button type="submit" className="btn btn-secondary">
                  Log out
                </button>
              </form>
            </>
          ) : (
            <>
              <Link href="/login">Log in</Link>
              <Link href="/signup" className="btn btn-primary">
                Sign up
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
