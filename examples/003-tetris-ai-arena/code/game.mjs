import { COLORS, COLS, ROWS, clearLines, collides, createBoard, createPiece, merge, rotateMatrix } from "../../001-tetris-basic/code/game-core.mjs";
import { buildActionPlan, choosePlacement } from "../../002-tetris-ai/code/ai-core.mjs";
import { chooseRandomPlacement, makeRandom, pieceSequence } from "./arena-core.mjs";

const BLOCK = 22;
const ACTION_INTERVAL = 100;
const PIECE_LIMIT = 40;
const seed = 0x003a11;
const sequence = pieceSequence(seed, PIECE_LIMIT);
const status = document.querySelector("#status");
const pauseButton = document.querySelector("#pause");
let paused = false;
let lastAction = performance.now();

function contender(id, choose, random) {
  const canvas = document.querySelector(`#${id}-board`);
  return {
    id, choose, random, canvas, context: canvas.getContext("2d"),
    board: createBoard(), active: null, decision: null, actions: [],
    index: 0, lines: 0, done: false, illegal: 0,
  };
}

let contenders;

function updateReadout(entry) {
  document.querySelector(`#${entry.id}-pieces`).textContent = entry.index;
  document.querySelector(`#${entry.id}-lines`).textContent = entry.lines;
  document.querySelector(`#${entry.id}-input`).textContent = entry.actions[0] ?? (entry.done ? "finished" : "lock");
}

function plan(entry) {
  if (entry.index >= sequence.length) {
    entry.done = true;
    updateReadout(entry);
    return;
  }
  const kind = sequence[entry.index];
  entry.decision = entry.choose(entry.board, kind, entry.random);
  if (!entry.decision) {
    entry.done = true;
    updateReadout(entry);
    return;
  }
  entry.active = createPiece(kind);
  entry.actions = buildActionPlan(entry.active.x, entry.decision);
  updateReadout(entry);
}

function fail(entry) {
  entry.illegal += 1;
  entry.done = true;
  updateReadout(entry);
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
    if (collides(entry.board, entry.active, 0, 0, matrix)) return fail(entry);
    entry.active.matrix = matrix;
  } else {
    const [x, y] = action === "left" ? [-1, 0] : action === "right" ? [1, 0] : [0, 1];
    if (collides(entry.board, entry.active, x, y)) return fail(entry);
    entry.active.x += x;
    entry.active.y += y;
  }
  updateReadout(entry);
}

function drawCell(context, x, y, kind, alpha = 1) {
  context.globalAlpha = alpha;
  context.fillStyle = COLORS[kind];
  context.fillRect(x * BLOCK + 1, y * BLOCK + 1, BLOCK - 2, BLOCK - 2);
  context.globalAlpha = 1;
}

function draw(entry) {
  const { context, canvas } = entry;
  context.fillStyle = "#e9eef0";
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.strokeStyle = "rgba(11, 31, 42, .08)";
  for (let x = 1; x < COLS; x += 1) {
    context.beginPath(); context.moveTo(x * BLOCK + .5, 0); context.lineTo(x * BLOCK + .5, canvas.height); context.stroke();
  }
  for (let y = 1; y < ROWS; y += 1) {
    context.beginPath(); context.moveTo(0, y * BLOCK + .5); context.lineTo(canvas.width, y * BLOCK + .5); context.stroke();
  }
  entry.board.forEach((row, y) => row.forEach((kind, x) => kind && drawCell(context, x, y, kind)));
  if (entry.active && !entry.done) entry.active.matrix.forEach((row, y) => row.forEach((filled, x) => {
    if (filled) drawCell(context, entry.active.x + x, entry.active.y + y, entry.active.kind);
  }));
}

function reset() {
  contenders = [
    contender("random", chooseRandomPlacement, makeRandom(seed ^ 0x9e3779b9)),
    contender("heuristic", choosePlacement, () => 0),
  ];
  contenders.forEach(plan);
  paused = false;
  pauseButton.textContent = "Pause match";
  status.textContent = "Same pieces. One legal input per agent every 100 ms.";
  lastAction = performance.now();
}

function frame(timestamp) {
  if (!paused && timestamp - lastAction >= ACTION_INTERVAL) {
    contenders.forEach(act);
    lastAction = timestamp;
    if (contenders.every((entry) => entry.done)) {
      paused = true;
      const [random, heuristic] = contenders;
      const winner = heuristic.lines > random.lines ? "Heuristic wins" : heuristic.lines < random.lines ? "Random wins" : "Draw";
      status.textContent = `${winner}: ${heuristic.lines}–${random.lines} lines on the same ${PIECE_LIMIT}-piece stream.`;
      pauseButton.textContent = "Match complete";
    }
  }
  contenders.forEach(draw);
  requestAnimationFrame(frame);
}

pauseButton.addEventListener("click", () => {
  if (contenders.every((entry) => entry.done)) return;
  paused = !paused;
  pauseButton.textContent = paused ? "Resume match" : "Pause match";
  status.textContent = paused ? "Match paused." : "Match resumed.";
  lastAction = performance.now();
});
document.querySelector("#restart").addEventListener("click", reset);

reset();
requestAnimationFrame(frame);
