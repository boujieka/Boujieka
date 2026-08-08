export function EmptyState({ message }: { message: string }) {
  return (
    <div className="flex flex-col items-center gap-1 rounded-xl border border-dashed border-zinc-300 px-6 py-12 text-center dark:border-zinc-700">
      <p className="text-sm text-zinc-500 dark:text-zinc-400">{message}</p>
    </div>
  );
}
