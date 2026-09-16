import type { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'BOUNCAMPUS — Mission Control for Boğaziçi',
    short_name: 'BOUNCAMPUS',
    description: 'Source-traceable campus decision intelligence: missions, counterfactuals, human approval and calibration evidence.',
    start_url: '/',
    display: 'standalone',
    background_color: '#f4f5f2',
    theme_color: '#0b1226',
    orientation: 'portrait-primary',
    categories: ['education', 'productivity', 'utilities'],
  };
}
