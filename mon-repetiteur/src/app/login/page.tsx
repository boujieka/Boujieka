import { LoginForm } from "./login-form";

export default function LoginPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-sm flex-col justify-center gap-6 px-6">
      <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
        Se connecter
      </h1>
      <LoginForm />
    </main>
  );
}
