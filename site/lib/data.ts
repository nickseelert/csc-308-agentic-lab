// Typed access to JSON written by `python -m analysis.build_site_data`.
import summaryJson from "@/data/summary.json";
import velocityJson from "@/data/velocity_leaders.json";
import strikeoutJson from "@/data/strikeout_leaders.json";
import pitchMixJson from "@/data/pitch_mix.json";
import hardestJson from "@/data/hardest_hit.json";

export type Summary = {
  pitches: number;
  games: number;
  first_date: string;
  last_date: string;
  home_runs: number;
  strikeouts: number;
  max_velo: number;
  max_exit_velo: number;
  whiff_rate: number;
};
export type VelocityLeader = { pitcher: string; avg_velo: number; max_velo: number; pitches: number };
export type StrikeoutLeader = { pitcher: string; strikeouts: number; batters_faced: number };
export type PitchMix = { pitch: string; count: number; share: number };
export type HardHit = {
  batter: string;
  exit_velo: number;
  launch_angle: number | null;
  result: string | null;
  date: string;
  round: string;
};

export const summary = summaryJson as Summary;
export const velocityLeaders = velocityJson as VelocityLeader[];
export const strikeoutLeaders = strikeoutJson as StrikeoutLeader[];
export const pitchMix = pitchMixJson as PitchMix[];
export const hardestHit = hardestJson as HardHit[];
