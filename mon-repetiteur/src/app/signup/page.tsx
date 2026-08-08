import { SignupForm } from "./signup-form";

export default function SignupPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-sm flex-col justify-center gap-6 px-6">
      <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
        Créer un compte
      </h1>
      <SignupForm />
    </main>
  );
}
