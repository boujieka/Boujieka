/** Logo ATEN — « Le disque solaire » : disque or sur fond navy, arc vert. */
export function Logo({ size = 32 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 48 48" aria-hidden>
      <circle cx="24" cy="24" r="22" fill="#0A1E3F" />
      <circle cx="24" cy="24" r="12" fill="#C9A227" />
      <path
        d="M24 6 A18 18 0 0 1 42 24"
        fill="none"
        stroke="#1FA36A"
        strokeWidth="3.5"
        strokeLinecap="round"
      />
      {Array.from({ length: 8 }).map((_, i) => {
        const a = (i / 8) * Math.PI * 2;
        const x1 = 24 + Math.cos(a) * 15;
        const y1 = 24 + Math.sin(a) * 15;
        const x2 = 24 + Math.cos(a) * 19;
        const y2 = 24 + Math.sin(a) * 19;
        return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#C9A227" strokeWidth="2" strokeLinecap="round" />;
      })}
    </svg>
  );
}

export function Wordmark() {
  return (
    <span className="flex items-center gap-2">
      <Logo size={28} />
      <span className="text-lg font-semibold tracking-tight text-navy-800">
        ATEN <span className="font-normal text-navy-400">· Le disque solaire</span>
      </span>
    </span>
  );
}
