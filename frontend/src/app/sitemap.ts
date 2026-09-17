import type { MetadataRoute } from 'next';
import { getSiteUrl } from '@/lib/site-url';

export default function sitemap(): MetadataRoute.Sitemap {
  const base = getSiteUrl();
  const now = new Date();
  return [
    { url: `${base}/`, lastModified: now, changeFrequency: 'daily', priority: 1 },
    { url: `${base}/food-waste`, lastModified: now, changeFrequency: 'daily', priority: 0.98 },
    { url: `${base}/demo`, lastModified: now, changeFrequency: 'daily', priority: 0.95 },
    { url: `${base}/food-waste/pilot`, lastModified: now, changeFrequency: 'daily', priority: 0.94 },
    { url: `${base}/decisions`, lastModified: now, changeFrequency: 'daily', priority: 0.9 },
    { url: `${base}/data`, lastModified: now, changeFrequency: 'daily', priority: 0.9 },
    { url: `${base}/buildings`, lastModified: now, changeFrequency: 'weekly', priority: 0.75 },
    { url: `${base}/mobility`, lastModified: now, changeFrequency: 'daily', priority: 0.72 },
    { url: `${base}/courses`, lastModified: now, changeFrequency: 'weekly', priority: 0.7 },
    { url: `${base}/scenarios`, lastModified: now, changeFrequency: 'weekly', priority: 0.68 },
  ];
}
