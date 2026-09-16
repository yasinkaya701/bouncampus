import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

async function readJson(url: URL, signal: AbortSignal) {
  const response = await fetch(url, { cache: 'no-store', signal });
  if (!response.ok) throw new Error(`${url.pathname} returned ${response.status}`);
  return response.json();
}

export async function GET(request: Request) {
  const started = Date.now();
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 9000);

  try {
    const healthUrl = new URL('/api/v1/health', request.url);
    const briefUrl = new URL('/api/v1/brief', request.url);
    const [health, brief] = await Promise.all([
      readJson(healthUrl, controller.signal),
      readJson(briefUrl, controller.signal),
    ]);

    const coreReady = Boolean(brief?.date && brief?.source_health?.total > 0);
    const payload = {
      ready: coreReady,
      status: coreReady ? 'ready' : 'not_ready',
      checked_at: new Date().toISOString(),
      latency_ms: Date.now() - started,
      release: {
        commit: process.env.VERCEL_GIT_COMMIT_SHA ?? process.env.GIT_COMMIT_SHA ?? 'local',
        environment: process.env.VERCEL_ENV ?? process.env.NODE_ENV ?? 'development',
        region: process.env.VERCEL_REGION ?? 'local',
      },
      dependencies: {
        health: health?.status ?? 'unknown',
        mission: brief?.status ?? 'unknown',
        upstream_passing: brief?.source_health?.passing ?? 0,
        upstream_total: brief?.source_health?.total ?? 0,
      },
      note: 'A degraded public source does not make the application unavailable; provenance and confidence expose degraded inputs explicitly.',
    };

    return NextResponse.json(payload, {
      status: coreReady ? 200 : 503,
      headers: { 'Cache-Control': 'no-store' },
    });
  } catch (error) {
    return NextResponse.json({
      ready: false,
      status: 'not_ready',
      checked_at: new Date().toISOString(),
      latency_ms: Date.now() - started,
      error: error instanceof Error ? error.message : String(error),
    }, {
      status: 503,
      headers: { 'Cache-Control': 'no-store' },
    });
  } finally {
    clearTimeout(timer);
  }
}
