import { runMatch, summarize } from "./arena-core.mjs";

const seeds = Number(process.argv[2] ?? 50);
const pieceLimit = Number(process.argv[3] ?? 300);
const matches = Array.from({ length: seeds }, (_, index) => runMatch(index + 1, pieceLimit));
console.log(JSON.stringify({ pieceLimit, ...summarize(matches), results: matches }, null, 2));
