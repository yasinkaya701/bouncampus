import type { DashboardData } from './types';
import type { SourceMeta } from './live-sources';

export interface MissionEvidence {
  id: string;
  label: string;
  value: string;
  interpretation: string;
  source?: SourceMeta;
}

export interface MissionImpact {
  label: string;
  value: number;
  unit: string;
  note: string;
}

export interface MissionBrief {
  generated_at: string;
  date: string;
  status: 'READY' | 'WATCH' | 'DEGRADED';
  title: string;
  one_liner: string;
  why_now: string;
  confidence: number;
  confidence_label: 'HIGH' | 'MEDIUM' | 'LOW';
  decision_id: string | null;
  decision_type: 'energy' | 'food' | 'space' | null;
  location: string;
  operating_window: string;
  recommendation: string;
  guardrail: string;
  evidence: MissionEvidence[];
  impact: MissionImpact[];
  source_health: {
    passing: number;
    total: number;
    official_live: number;
    external_live: number;
    unavailable: number;
  };
  dashboard: DashboardData;
}
