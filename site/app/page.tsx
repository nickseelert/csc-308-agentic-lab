import PitchMixChart from "@/components/PitchMixChart";
import { hardestHit, pitchMix, strikeoutLeaders, summary, velocityLeaders } from "@/lib/data";

export default function Home() {
  const s = summary;
  return (
    <main>
      <h1>2026 Postseason, pitch by pitch</h1>
      <p className="lede">
        Public MLB Statcast data from {s.first_date} to {s.last_date}. Every feature on this page
        was requested in class and built by a team of AI agents through issues, pull requests,
        review and CI.
      </p>

      <section className="stats" aria-label="Headline numbers">
        <div className="stat"><b>{s.pitches.toLocaleString()}</b><span>pitches</span></div>
        <div className="stat"><b>{s.games}</b><span>games</span></div>
        <div className="stat"><b>{s.home_runs}</b><span>home runs</span></div>
        <div className="stat"><b>{s.strikeouts}</b><span>strikeouts</span></div>
        <div className="stat"><b>{s.max_velo}</b><span>fastest pitch (mph)</span></div>
        <div className="stat"><b>{(s.whiff_rate * 100).toFixed(1)}%</b><span>whiff rate</span></div>
      </section>

      <h2>Pitch mix</h2>
      <PitchMixChart data={pitchMix} />

      <h2>Hardest four-seamers (avg velocity, min 25 pitches)</h2>
      <table>
        <thead>
          <tr><th>Pitcher</th><th className="num">Avg mph</th><th className="num">Max mph</th><th className="num">Pitches</th></tr>
        </thead>
        <tbody>
          {velocityLeaders.map((r) => (
            <tr key={r.pitcher}>
              <td>{r.pitcher}</td>
              <td className="num">{r.avg_velo}</td>
              <td className="num">{r.max_velo}</td>
              <td className="num">{r.pitches}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Strikeout leaders (top 10)</h2>
      <p className="lede">
        K counts strikeouts, including strikeout double plays. BF is batters faced: completed plate
        appearances, not individual pitches. Figures cover the committed 2026 postseason snapshot
        only, not live results.
      </p>
      <table>
        <thead>
          <tr><th>Pitcher</th><th className="num">K</th><th className="num">BF</th></tr>
        </thead>
        <tbody>
          {strikeoutLeaders.map((r, i) => (
            <tr key={`${r.pitcher}-${i}`}>
              <td>{r.pitcher}</td>
              <td className="num">{r.strikeouts}</td>
              <td className="num">{r.batters_faced}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Hardest-hit balls</h2>
      <table>
        <thead>
          <tr><th>Batter</th><th className="num">Exit velo</th><th className="num">Launch angle</th><th>Result</th><th>Round</th><th>Date</th></tr>
        </thead>
        <tbody>
          {hardestHit.map((r, i) => (
            <tr key={`${r.batter}-${r.date}-${i}`}>
              <td>{r.batter}</td>
              <td className="num">{r.exit_velo}</td>
              <td className="num">{r.launch_angle ?? "—"}</td>
              <td>{r.result ?? "—"}</td>
              <td>{r.round}</td>
              <td>{r.date}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <footer>
        Data: MLB Statcast via <a href="https://github.com/jldbc/pybaseball">pybaseball</a>. Built for
        a University of Toronto CSC308 guest lecture.{" "}
        <a href="https://github.com/nickseelert/csc-308-agentic-lab">Source, issues and PRs</a>.
      </footer>
    </main>
  );
}
