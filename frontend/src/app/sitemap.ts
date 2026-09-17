import type { MetadataRoute } from 'next';
import { getSiteUrl } from '@/lib/site-url';

export default function sitemap(): MetadataRoute.Sitemap {
  const base = getSiteUrl();
  const now = new Date();
  return [
    { url: `${base}/`, lastModified: now, changeFrequency: 'daily', priority: 1 },
    { url: `${base}/demo`, lastModified: now, changeFrequency: 'daily', priority: 0.95 },
    { url: `${base}/decisions`, lastModified: now, changeFrequency: 'daily', priority: 0.9 },
    { url: `${base}/buildings`, lastModified: now, changeFrequency: 'weekly', priority: 0.8 },
    { url: `${base}/mobility`, lastModified: now, changeFrequency: 'daily', priority: 0.85 },
    { url: `${base}/courses`, lastModified: now, changeFrequency: 'weekly', priority: 0.8 },
    { url: `${base}/scenarios`, lastModified: now, changeFrequency: 'weekly', priority: 0.75 },
    { url: `${base}/data`, lastModified: now, changeFrequency: 'daily', priority: 0.75 },
  ];
}
