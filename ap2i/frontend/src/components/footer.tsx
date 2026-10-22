import Link from "next/link";
import type { Dict } from "@/i18n";

export function Footer({ d }: { d: Dict }) {
  return (
    <footer className="mt-12 border-t border-line bg-white">
      <div className="mx-auto grid max-w-7xl gap-4 px-4 py-6 text-sm text-muted md:grid-cols-3">
        <div>
          <p className="font-semibold text-navy">{d.footer.rights}</p>
          <p className="mt-1 italic">{d.meta.tagline}</p>
        </div>
        <div>
          <p>{d.footer.dataFrom}</p>
          <p className="mt-1">{d.footer.mapCredit}</p>
        </div>
        <div className="flex flex-wrap gap-x-4 gap-y-1 md:justify-end">
          <Link className="link" href="/about">{d.nav.about}</Link>
          <Link className="link" href="/methodology">{d.nav.methodology}</Link>
          <Link className="link" href="/explorer#quality">{d.explorer.quality}</Link>
          <Link className="link" href="/pricing">{d.nav.pricing}</Link>
        </div>
      </div>
    </footer>
  );
}
