import { NextResponse } from "next/server";
import { hasApiKey } from "@/lib/ai/claude";

export async function GET() {
  return NextResponse.json({
    status: "ok",
    service: "ATEN",
    aiConfigured: hasApiKey(),
    timestamp: new Date().toISOString(),
  });
}
