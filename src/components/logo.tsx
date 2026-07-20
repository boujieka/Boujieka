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

/** Grand disque solaire décoratif (hero landing) — couronne de rayons animée. */
export function SolarDisc({ className = "" }: { className?: string }) {
  const rays = Array.from({ length: 16 }).map((_, i) => {
    const a = (i / 16) * Math.PI * 2;
    const c = 100;
    const x1 = c + Math.cos(a) * 54;
    const y1 = c + Math.sin(a) * 54;
    const x2 = c + Math.cos(a) * 66;
    const y2 = c + Math.sin(a) * 66;
    return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} />;
  });
  return (
    <svg viewBox="0 0 200 200" className={className} aria-hidden>
      <defs>
        <radialGradient id="aten-sun" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#e9d084" />
          <stop offset="60%" stopColor="#c9a227" />
          <stop offset="100%" stopColor="#a9871c" />
        </radialGradient>
      </defs>
      <g className="aten-spin" stroke="#c9a227" strokeWidth={2.4} strokeLinecap="round" opacity={0.5}>
        {rays}
      </g>
      <circle cx={100} cy={100} r={46} fill="url(#aten-sun)" />
      <path d="M100 40 A60 60 0 0 1 160 100" fill="none" stroke="#1fa36a" strokeWidth={5} strokeLinecap="round" />
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
