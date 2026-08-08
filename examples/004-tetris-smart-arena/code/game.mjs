import { COLORS, clearLines, collides, createBoard, createPiece, merge, rotateMatrix } from "../../001-tetris-basic/code/game-core.mjs";
import { buildActionPlan } from "../../002-tetris-ai/code/ai-core.mjs";
import { pieceSequence } from "../../003-tetris-ai-arena/code/arena-core.mjs";
import { chooseGreedyPlacement, chooseLookaheadPlacement, futureScoreFor } from "./smart-core.mjs";

const BLOCK = 20;
const ACTION_INTERVAL = 100;
const PIECE_LIMIT = 40;
const seed = 0x004a11;
const sequence = pieceSequence(seed, PIECE_LIMIT);
const status = document.querySelector("#status");
const pauseButton = document.querySelector("#pause");
let paused = false;
let lastAction = performance.now();
let agents;
let divergences;

function makeAgent(id, choose) {
  const canvas = document.querySelector(`#${id}-board`);
  return {
    id, choose, canvas, context: canvas.getContext("2d"), board: createBoard(),
    active: null, decision: null, actions: [], index: 0, lines: 0, done: false,
  };
}

function text(id, value) { document.querySelector(`#${id}`).textContent = value; }

function update(entry) {
  text(`${entry.id}-pieces`, entry.index);
  text(`${entry.id}-lines`, entry.lines);
  text(`${entry.id}-input`, entry.actions[0] ?? (entry.done ? "finished" : "lock"));
  if (!entry.decision) return;
  text(`${entry.id}-column`, entry.decision.x + 1);
  text(`${entry.id}-now`, entry.decision.immediateScore);
  text(`${entry.id}-future`, entry.decision.futureScore ?? "not checked");
}

function explainLookahead(entry, kind, nextKind) {
  const greedy = chooseGreedyPlacement(entry.board, kind);
  const greedyFuture = futureScoreFor(greedy, nextKind);
  const changed = greedy.x !== entry.decision.x || greedy.rotation !== entry.decision.rotation;
  if (changed) divergences += 1;
  text("current-piece", kind);
  text("next-piece", nextKind ?? "—");
  text("now-choice", `column ${greedy.x + 1} · ${greedy.immediateScore}`);
  text("future-choice", `column ${entry.decision.x + 1} · ${entry.decision.futureScore}`);
  text("branches", `${entry.decision.replies} replies`);
  text("divergences", divergences);
  text("reason", changed
    ? `Foresight changed the move: it compared the next ${nextKind} after every legal ${kind} landing.`
    : `Both methods agree here; foresight still checked every legal reply for the next ${nextKind}.`);
  text("future-gain", entry.decision.futureScore - greedyFuture);
}

function plan(entry) {
  if (entry.index >= sequence.length) { entry.done = true; update(entry); return; }
  const kind = sequence[entry.index];
  const nextKind = sequence[entry.index + 1];
  entry.decision = entry.choose(entry.board, kind, nextKind);
  if (!entry.decision) { entry.done = true; update(entry); return; }
  entry.active = createPiece(kind);
  entry.actions = buildActionPlan(entry.active.x, entry.decision);
  if (entry.id === "lookahead") explainLookahead(entry, kind, nextKind);
  update(entry);
}

function lock(entry) {
  entry.board = merge(entry.board, entry.active);
  const result = clearLines(entry.board);
  entry.board = result.board;
  entry.lines += result.lines;
  entry.index += 1;
  plan(entry);
}

function act(entry) {
  if (entry.done) return;
  const action = entry.actions.shift();
  if (!action) return lock(entry);
  if (action === "rotate") {
    const matrix = rotateMatrix(entry.active.matrix);
    if (collides(entry.board, entry.active, 0, 0, matrix)) return void (entry.done = true);
    entry.active.matrix = matrix;
  } else {
    const [x, y] = action === "left" ? [-1, 0] : action === "right" ? [1, 0] : [0, 1];
    if (collides(entry.board, entry.active, x, y)) return void (entry.done = true);
    entry.active.x += x;
    entry.active.y += y;
  }
  update(entry);
}

function drawCell(context, x, y, kind) {
  context.fillStyle = COLORS[kind];
  context.fillRect(x * BLOCK + 1, y * BLOCK + 1, BLOCK - 2, BLOCK - 2);
}

function draw(entry) {
  const { context, canvas } = entry;
  context.fillStyle = "#f2f0f7";
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.strokeStyle = "rgba(34, 29, 53, .08)";
  for (let x = 1; x < 10; x += 1) { context.beginPath(); context.moveTo(x * BLOCK + .5, 0); context.lineTo(x * BLOCK + .5, canvas.height); context.stroke(); }
  for (let y = 1; y < 20; y += 1) { context.beginPath(); context.moveTo(0, y * BLOCK + .5); context.lineTo(canvas.width, y * BLOCK + .5); context.stroke(); }
  entry.board.forEach((row, y) => row.forEach((kind, x) => kind && drawCell(context, x, y, kind)));
  if (entry.active && !entry.done) entry.active.matrix.forEach((row, y) => row.forEach((filled, x) => filled && drawCell(context, entry.active.x + x, entry.active.y + y, entry.active.kind)));
}

function reset() {
  divergences = 0;
  agents = [makeAgent("greedy", chooseGreedyPlacement), makeAgent("lookahead", chooseLookaheadPlacement)];
  agents.forEach(plan);
  paused = false;
  pauseButton.textContent = "Pause duel";
  status.textContent = "Same pieces. Same 100 ms clock. Different planning depth.";
  lastAction = performance.now();
}

function frame(timestamp) {
  if (!paused && timestamp - lastAction >= ACTION_INTERVAL) {
    agents.forEach(act);
    lastAction = timestamp;
    if (agents.every((entry) => entry.done)) {
      paused = true;
      const [greedy, lookahead] = agents;
      status.textContent = `Duel complete: lookahead ${lookahead.lines}, greedy ${greedy.lines} lines.`;
      pauseButton.textContent = "Duel complete";
    }
  }
  agents.forEach(draw);
  requestAnimationFrame(frame);
}

pauseButton.addEventListener("click", () => {
  if (agents.every((entry) => entry.done)) return;
  paused = !paused;
  pauseButton.textContent = paused ? "Resume duel" : "Pause duel";
  status.textContent = paused ? "Duel paused." : "Duel resumed.";
  lastAction = performance.now();
});
document.querySelector("#restart").addEventListener("click", reset);

reset();
requestAnimationFrame(frame);
