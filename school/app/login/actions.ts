"use server";

import { z } from "zod";
import { redirect } from "next/navigation";
import { findUserByEmail, verifyPassword } from "@/lib/auth";
import { createSession } from "@/lib/session";

const schema = z.object({
  email: z.string().email("Enter a valid email."),
  password: z.string().min(1, "Password is required."),
  next: z.string().optional(),
});

export type LoginState = { error?: string };

export async function login(_prevState: LoginState, formData: FormData): Promise<LoginState> {
  const parsed = schema.safeParse({
    email: formData.get("email"),
    password: formData.get("password"),
    next: formData.get("next") ?? undefined,
  });

  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Invalid input." };
  }

  const { email, password, next } = parsed.data;

  const user = await findUserByEmail(email);
  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    return { error: "Incorrect email or password." };
  }

  await createSession({ userId: user.id, role: user.role });
  redirect(next && next.startsWith("/") ? next : "/dashboard");
}
