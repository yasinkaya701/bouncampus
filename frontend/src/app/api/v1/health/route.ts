import { NextResponse } from 'next/server';
import { fetchBounCalendar, fetchBounMenu, fetchBounShuttle, fetchBounWeather } from '@/lib/live-sources';

export async function GET() {
  const startedAt = Date.now();
  const feeds = await Promise.all([
    fetchBounMenu(),
    fetchBounShuttle(),
    fetchBounCalendar(),
    fetchBounWeather(),
  ]);

  const sources = feeds.map(feed => feed.source);
  const failed = sources.filter(source => !source.ok);

  return NextResponse.json({
    status: failed.length === 0 ? 'ok' : 'degraded',
    checked_at: new Date().toISOString(),
    latency_ms: Date.now() - startedAt,
    sources,
    failed_source_ids: failed.map(source => source.id),
  }, {
    status: failed.length === sources.length ? 503 : 200,
  });
}
