import { Alert } from "@/components/ui/alert";
import type { Dict } from "@/i18n";

/** Coverage disclaimer shown on every dashboard. `apiText` shows the API's own coverage statement verbatim. */
export function CoverageNotice({ d, apiText, className }: { d: Dict; apiText?: string | null; className?: string }) {
  return (
    <Alert tone="warning" title={d.coverage.title} className={className}>
      <p>{d.coverage.text}</p>
      {apiText ? <p className="mt-1 text-xs opacity-90">API: “{apiText}”</p> : null}
    </Alert>
  );
}
