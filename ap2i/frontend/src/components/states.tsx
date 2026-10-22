import Link from "next/link";
import { Alert } from "@/components/ui/alert";
import { buttonClass } from "@/components/ui/button";
import type { Dict } from "@/i18n";

export function ErrorState({ d, status, message }: { d: Dict; status?: number; message?: string }) {
  return (
    <Alert tone="danger" title={`${d.common.error}${status ? ` ${status}` : ""}`}>
      <p>{d.common.apiError}</p>
      {message ? <p className="mt-1 font-mono text-xs break-anywhere">{message}</p> : null}
    </Alert>
  );
}

export function LoginRequired({ d, next }: { d: Dict; next: string }) {
  return (
    <Alert tone="info" title={d.common.loginRequired}>
      <p>{d.common.loginToAccess}</p>
      <div className="mt-3 flex flex-wrap gap-2">
        <Link href={`/login?next=${encodeURIComponent(next)}`} className={buttonClass("primary", "sm")}>{d.nav.login}</Link>
        <Link href="/register" className={buttonClass("outline", "sm")}>{d.nav.register}</Link>
      </div>
    </Alert>
  );
}

export function UpgradeRequired({ d, detail }: { d: Dict; detail?: string }) {
  return (
    <Alert tone="warning" title={d.common.upgradeRequired}>
      <p>{d.common.upgradeText}</p>
      {detail ? <p className="mt-1 text-xs break-anywhere">API: “{detail}”</p> : null}
      <div className="mt-3">
        <Link href="/pricing" className={buttonClass("primary", "sm")}>{d.common.seePricing}</Link>
      </div>
    </Alert>
  );
}

export function Forbidden({ d }: { d: Dict }) {
  return <Alert tone="danger" title={d.common.forbidden} />;
}
