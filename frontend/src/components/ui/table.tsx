import * as React from "react";

import { cn } from "@/lib/utils";

export function Table({ className, ...props }: React.ComponentProps<"table">) {
  return (
    <div className="w-full overflow-x-auto">
      <table className={cn("w-full border-collapse text-[13px]", className)} {...props} />
    </div>
  );
}

export function THead(props: React.ComponentProps<"thead">) {
  return <thead {...props} />;
}

export function TBody(props: React.ComponentProps<"tbody">) {
  return <tbody {...props} />;
}

export function TR({ className, ...props }: React.ComponentProps<"tr">) {
  return (
    <tr
      className={cn("border-b border-border last:border-0 hover:bg-surface-2/60", className)}
      {...props}
    />
  );
}

export function TH({ className, ...props }: React.ComponentProps<"th">) {
  return (
    <th
      scope="col"
      className={cn(
        "border-b border-border-strong bg-surface-2/50 px-3 py-2 text-left text-[11px] font-semibold uppercase tracking-wide text-muted whitespace-nowrap",
        className,
      )}
      {...props}
    />
  );
}

export function TD({ className, ...props }: React.ComponentProps<"td">) {
  return <td className={cn("px-3 py-1.5 align-top whitespace-nowrap", className)} {...props} />;
}
