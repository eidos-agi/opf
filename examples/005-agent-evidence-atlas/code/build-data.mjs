import { writeFileSync } from "node:fs";
import { runMatch, summarize } from "../../003-tetris-ai-arena/code/arena-core.mjs";
import { runSmartMatch, summarizeSmart } from "../../004-tetris-smart-arena/code/smart-core.mjs";

const generatedAt = "2026-08-08T00:10:00Z";
const baselineMatches = Array.from({ length: 50 }, (_, index) => runMatch(index + 1, 300));
const smartMatches = Array.from({ length: 50 }, (_, index) => runSmartMatch(index + 1, 300));
const baseline = summarize(baselineMatches);
const smart = summarizeSmart(smartMatches);
const lineLift = (smart.lookaheadLines - smart.greedyLines) / smart.greedyLines;

const deltaBins = [
  { label: "−1 line", min: -1, max: -1 },
  { label: "Tie", min: 0, max: 0 },
  { label: "+1–2", min: 1, max: 2 },
  { label: "+3–5", min: 3, max: 5 },
  { label: "+6–10", min: 6, max: 10 },
  { label: "+11 or more", min: 11, max: Infinity },
];
const deltas = smartMatches.map((match) => match.lookahead.lines - match.greedy.lines);
const deltaDistribution = deltaBins.map((bin) => {
  const values = deltas.filter((delta) => delta >= bin.min && delta <= bin.max);
  return {
    difference: bin.label,
    seeds: values.length,
    min_delta: values.length ? Math.min(...values) : null,
    max_delta: values.length ? Math.max(...values) : null,
  };
});
const cohortSummary = [
  { experiment: "003", comparison: "Heuristic vs random legal", matches: baseline.matches, winner_lines: baseline.heuristicLines, comparison_lines: baseline.randomLines, illegal_moves: baseline.illegalMoves },
  { experiment: "004", comparison: "Lookahead vs greedy", matches: smart.matches, winner_lines: smart.lookaheadLines, comparison_lines: smart.greedyLines, illegal_moves: smart.illegalMoves },
];
const sqlRows = [
  ["headline", "all", "baseline_win_rate", baseline.heuristicWins / baseline.matches],
  ["headline", "all", "line_lift", lineLift],
  ["headline", "all", "extra_lines", smart.lookaheadLines - smart.greedyLines],
  ["headline", "all", "extra_pieces", smart.lookaheadPieces - smart.greedyPieces],
  ["headline", "all", "illegal_moves", baseline.illegalMoves + smart.illegalMoves],
  ["baseline_summary", "Random legal", "lines", baseline.randomLines],
  ["baseline_summary", "One-piece heuristic", "lines", baseline.heuristicLines],
  ["foresight_outcomes", "Wins", "matches", smart.lookaheadWins],
  ["foresight_outcomes", "Draws", "matches", smart.draws],
  ["foresight_outcomes", "Losses", "matches", smart.greedyWins],
  ...deltaDistribution.map((row) => ["delta_distribution", row.difference, "seeds", row.seeds]),
  ...cohortSummary.flatMap((row) => [
    ["cohort_summary", row.experiment, "winner_lines", row.winner_lines],
    ["cohort_summary", row.experiment, "comparison_lines", row.comparison_lines],
    ["cohort_summary", row.experiment, "illegal_moves", row.illegal_moves],
  ]),
];
const sqlValue = (value) => typeof value === "number" ? String(value) : `'${String(value).replaceAll("'", "''")}'`;
const snapshotSql = [
  "WITH evidence(dataset, category, metric, value) AS (",
  `  VALUES ${sqlRows.map((row) => `(${row.map(sqlValue).join(", ")})`).join(",\n         ")}`,
  ")",
  "SELECT dataset, category, metric, value",
  "FROM evidence",
  "ORDER BY dataset, category, metric;",
].join("\n");

const source = {
  id: "cohort_pipeline",
  label: "Deterministic Tetris cohort pipeline",
  path: "examples/005-agent-evidence-atlas/code/build-data.mjs",
  query: {
    engine: "sqlite",
    language: "sql",
    sql: snapshotSql,
    description: "Reproduces the reviewed evaluator snapshot as normalized chart-source rows.",
    executed_at: generatedAt,
    filters: ["Seeds 1 through 50", "300-piece ceiling per match", "No sampled rows"],
    metric_definitions: [
      "Line lift = (lookahead lines − greedy lines) / greedy lines across 50 matched seeds.",
      "Win = strictly more cleared lines than the comparator on the same seeded piece stream.",
      "Illegal placement = a selected landing that fails collision or drop-distance validation.",
    ],
  },
};

const artifact = {
  surface: "dashboard",
  manifest: {
    version: 1,
    surface: "dashboard",
    title: "Agent Evidence Atlas",
    description: "Four maxims for making autonomous-agent claims falsifiable, demonstrated by the OPF Tetris series.",
    generatedAt,
    cards: [
      {
        id: "baseline_wins",
        description: "The one-piece heuristic beat the legal random control on every fixed seed.",
        dataset: "headline",
        sourceId: source.id,
        metrics: [
          { label: "Baseline wins", field: "baseline_win_rate", format: "percent" },
          { label: "Matches", field: "baseline_matches", format: "number" },
        ],
      },
      {
        id: "foresight_lift",
        description: "Additional cleared lines from seeing one known piece further ahead.",
        dataset: "headline",
        sourceId: source.id,
        metrics: [
          { label: "Line lift from foresight", field: "line_lift", format: "percent", signed: true },
          { label: "Extra lines", field: "extra_lines", format: "number", signed: true },
        ],
      },
      {
        id: "survival_gain",
        description: "Extra legal placements completed by lookahead across the same 50 streams.",
        dataset: "headline",
        sourceId: source.id,
        metrics: [
          { label: "Survival gain", field: "extra_pieces", format: "number", signed: true },
          { label: "Lookahead pieces", field: "lookahead_pieces", format: "number" },
        ],
      },
      {
        id: "illegal_moves",
        description: "Invalid placements across both comparison cohorts.",
        dataset: "headline",
        sourceId: source.id,
        metrics: [
          { label: "Illegal placements", field: "illegal_moves", format: "number" },
          { label: "Fixed-seed matches", field: "total_matches", format: "number" },
        ],
      },
    ],
    charts: [
      {
        id: "baseline_lines",
        title: "Aggregate lines by baseline strategy",
        subtitle: "50 fixed seeds · 300-piece ceiling per match · absolute line count starts at zero",
        type: "bar",
        dataset: "baseline_summary",
        sourceId: source.id,
        intent: "comparison",
        question: "Does the heuristic add value beyond merely choosing a legal move?",
        rationale: "A zero-based bar comparison makes the enormous baseline gap visible without transforming the scale.",
        palette: { kind: "semantic", name: "baseline-versus-candidate" },
        labels: { values: "all" },
        encodings: {
          x: { field: "agent", type: "nominal", label: "Strategy" },
          y: { field: "lines", type: "quantitative", label: "Lines cleared" },
          tooltip: [
            { field: "pieces", type: "quantitative", label: "Pieces placed" },
            { field: "wins", type: "quantitative", label: "Match wins" },
          ],
        },
        layout: "half",
      },
      {
        id: "foresight_record",
        title: "Depth-two match outcomes",
        subtitle: "Lookahead result against the depth-one heuristic · 50 fixed seeds",
        type: "bar",
        dataset: "foresight_outcomes",
        sourceId: source.id,
        intent: "composition",
        question: "How consistently does one-piece lookahead outperform the existing expert?",
        rationale: "Outcome counts distinguish wins, ties, and losses without hiding the four seeds where lookahead was worse.",
        palette: { kind: "categorical", name: "outcome-counts" },
        labels: { values: "all" },
        encodings: {
          x: { field: "outcome", type: "nominal", label: "Lookahead outcome" },
          y: { field: "matches", type: "quantitative", label: "Matches" },
        },
        layout: "half",
      },
      {
        id: "delta_distribution",
        title: "Per-seed line difference from foresight",
        subtitle: "Lookahead lines minus greedy lines · all 50 fixed seeds · zero means a draw",
        type: "bar",
        dataset: "delta_distribution",
        sourceId: source.id,
        intent: "distribution",
        question: "Is the aggregate foresight gain broad or driven by one exceptional seed?",
        rationale: "Binned signed differences reveal both the broad positive shift and the single large survival outlier.",
        palette: { kind: "sequential", name: "foresight-delta" },
        labels: { values: "all" },
        encodings: {
          x: { field: "difference", type: "ordinal", label: "Additional lines per seed" },
          y: { field: "seeds", type: "quantitative", label: "Seed count" },
          tooltip: [
            { field: "min_delta", type: "quantitative", label: "Minimum difference" },
            { field: "max_delta", type: "quantitative", label: "Maximum difference" },
          ],
        },
        layout: "full",
      },
    ],
    tables: [
      {
        id: "cohort_table",
        title: "Cohort audit",
        subtitle: "Exact totals behind the headline comparisons.",
        dataset: "cohort_summary",
        sourceId: source.id,
        defaultSort: { field: "experiment", direction: "asc" },
        columns: [
          { field: "experiment", label: "Experiment", type: "text" },
          { field: "comparison", label: "Comparison", type: "text" },
          { field: "matches", label: "Matches", format: "number" },
          { field: "winner_lines", label: "Winner lines", format: "number" },
          { field: "comparison_lines", label: "Comparator lines", format: "number" },
          { field: "illegal_moves", label: "Illegal moves", format: "number" },
        ],
      },
    ],
    sources: [source],
    blocks: [
      {
        id: "thesis",
        type: "markdown",
        body: "# Agent Evidence Atlas\n\n**Intelligence should earn its adjectives.** This atlas turns the first four OPF Tetris products into a compact argument for how autonomous systems should be demonstrated.",
      },
      { id: "headline_metrics", type: "metric-strip", cardIds: ["baseline_wins", "foresight_lift", "survival_gain", "illegal_moves"] },
      {
        id: "maxims",
        type: "markdown",
        body: "## Four maxims\n\n1. **Hold inputs constant.** Same seeded seven-bag streams make strategy the tested variable.\n2. **Prove legal before better.** Every agent must use ordinary actions; no teleporting and no invalid placements.\n3. **A baseline creates meaning.** Legal random play shows whether the first heuristic contributes judgment.\n4. **Expose mechanism, then measure outcome.** The depth-two agent shows its next-piece search and must still win a fixed cohort.",
      },
      { id: "baseline_chart", type: "chart", chartId: "baseline_lines" },
      { id: "record_chart", type: "chart", chartId: "foresight_record" },
      { id: "distribution_chart", type: "chart", chartId: "delta_distribution" },
      {
        id: "examples",
        type: "markdown",
        body: "## See the claims behave\n\n- [003 · Same bag, different judgment](/003-tetris-ai-arena/code/) compares a legal random control with the first heuristic.\n- [004 · One move further](/004-tetris-smart-arena/code/) shows the exact moment next-piece foresight changes a decision.\n\nBoth live examples restrict each agent to at most one normal input every 100 ms.",
      },
      { id: "audit_table", type: "table", tableId: "cohort_table" },
      {
        id: "method",
        type: "markdown",
        sourceId: source.id,
        body: "## Method\n\nThe snapshot reruns 100 deterministic matches: 50 random-versus-heuristic and 50 greedy-versus-lookahead, each capped at 300 offered pieces. Results are aggregate outcomes, not a claim of optimal Tetris play. The depth-two result includes 36 wins, 10 draws, and 4 losses; the losses remain visible because a stronger agent is not an infallible one.",
      },
    ],
  },
  snapshot: {
    version: 1,
    generatedAt,
    status: "ready",
    datasets: {
      headline: [{
        baseline_win_rate: baseline.heuristicWins / baseline.matches,
        baseline_matches: baseline.matches,
        line_lift: lineLift,
        extra_lines: smart.lookaheadLines - smart.greedyLines,
        extra_pieces: smart.lookaheadPieces - smart.greedyPieces,
        lookahead_pieces: smart.lookaheadPieces,
        illegal_moves: baseline.illegalMoves + smart.illegalMoves,
        total_matches: baseline.matches + smart.matches,
      }],
      baseline_summary: [
        { agent: "Random legal", lines: baseline.randomLines, pieces: baselineMatches.reduce((sum, match) => sum + match.random.pieces, 0), wins: 0 },
        { agent: "One-piece heuristic", lines: baseline.heuristicLines, pieces: baselineMatches.reduce((sum, match) => sum + match.heuristic.pieces, 0), wins: baseline.heuristicWins },
      ],
      foresight_outcomes: [
        { outcome: "Wins", matches: smart.lookaheadWins },
        { outcome: "Draws", matches: smart.draws },
        { outcome: "Losses", matches: smart.greedyWins },
      ],
      delta_distribution: deltaDistribution,
      cohort_summary: cohortSummary,
    },
  },
  sources: [source],
  package_info: {
    originUrl: "https://github.com/eidos-agi/opf/tree/main/examples/005-agent-evidence-atlas",
    sourceKind: "deterministic-local-snapshot",
  },
};

const output = process.argv[2] ?? new URL("artifact.json", import.meta.url).pathname;
writeFileSync(output, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ output, baseline, smart }, null, 2));
