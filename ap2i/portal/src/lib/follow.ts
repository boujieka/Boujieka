// Followed and recently viewed projects: stored only in this browser (never sent anywhere).
import { useCallback, useEffect, useState } from "react";

const FOLLOW = "ap2i.portal.followed";
const RECENT = "ap2i.portal.recent";
const EVT = "ap2i-follow-change";

function read(key: string): string[] {
  try {
    const v = JSON.parse(localStorage.getItem(key) ?? "[]");
    return Array.isArray(v) ? v.filter((x) => typeof x === "string" && /^[A-Z0-9_\-]{3,60}$/i.test(x)).slice(0, 50) : [];
  } catch {
    return [];
  }
}

function write(key: string, v: string[]) {
  try {
    localStorage.setItem(key, JSON.stringify(v.slice(0, 50)));
  } catch { /* storage unavailable (private mode): state kept for this page only */ }
  window.dispatchEvent(new Event(EVT));
}

export function useFollowed() {
  const [followed, setFollowed] = useState<string[]>(() => read(FOLLOW));
  const [recent, setRecent] = useState<string[]>(() => read(RECENT));
  useEffect(() => {
    const on = () => {
      setFollowed(read(FOLLOW));
      setRecent(read(RECENT));
    };
    window.addEventListener(EVT, on);
    window.addEventListener("storage", on);
    return () => {
      window.removeEventListener(EVT, on);
      window.removeEventListener("storage", on);
    };
  }, []);
  const toggle = useCallback((ref: string) => {
    const cur = read(FOLLOW);
    write(FOLLOW, cur.includes(ref) ? cur.filter((x) => x !== ref) : [ref, ...cur]);
  }, []);
  return { followed, recent, toggle, isFollowed: (ref: string) => followed.includes(ref) };
}

export function markViewed(ref: string) {
  write(RECENT, [ref, ...read(RECENT).filter((x) => x !== ref)].slice(0, 8));
}
