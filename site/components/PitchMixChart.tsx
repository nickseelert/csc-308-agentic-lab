"use client";

import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { PitchMix } from "@/lib/data";

export default function PitchMixChart({ data }: { data: PitchMix[] }) {
  const rows = data.map((d) => ({ ...d, pct: Math.round(d.share * 1000) / 10 }));
  return (
    <div className="chart">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={rows} layout="vertical" margin={{ left: 40, right: 20 }}>
          <XAxis type="number" unit="%" />
          <YAxis type="category" dataKey="pitch" width={130} />
          <Tooltip formatter={(v) => `${v}%`} />
          <Bar dataKey="pct" fill="#0b5cad" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
