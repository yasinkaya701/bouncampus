import type { Metadata } from 'next';
import ShuttleNetwork from '@/components/Mobility/ShuttleNetwork';

export const metadata: Metadata = {
  title: 'Mobility & Shuttle',
  description: 'Source-aware campus-loop and inter-campus shuttle planning for Boğaziçi University.',
};

export default function MobilityPage() {
  return <ShuttleNetwork />;
}
