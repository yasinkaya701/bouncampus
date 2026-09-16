import { NextResponse } from 'next/server';
import realCourses from '@/data/real_boun_courses.json';
import {
  courseScheduleSnapshotSource,
  fetchBounCalendar,
  fetchBounMenu,
  fetchBounShuttle,
  fetchBounWeather,
} from '@/lib/live-sources';

export const dynamic = 'force-dynamic';

export async function GET() {
  const startedAt = Date.now();
  const feeds = await Promise.all([
    fetchBounMenu(),
    fetchBounShuttle(),
    fetchBounCalendar(),
    fetchBounWeather(),
  ]);

  const courseCount = Object.keys(realCourses as Record<string, unknown>).length;
  const sources = [
    ...feeds.map(feed => feed.source),
    courseScheduleSnapshotSource(courseCount),
  ];
  const failed = sources.filter(source => !source.ok);

  return NextResponse.json({
    status: failed.length === 0 ? 'ok' : 'degraded',
    checked_at: new Date().toISOString(),
    latency_ms: Date.now() - startedAt,
    sources,
    failed_source_ids: failed.map(source => source.id),
  }, {
    status: failed.length === sources.length ? 503 : 200,
    headers: { 'Cache-Control': 'no-store' },
  });
}
