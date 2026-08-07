import {
  COLORS,
  COLS,
  ROWS,
  SHAPES,
  clearLines,
  collides,
  createBoard,
  createPiece,
  merge,
  rotateMatrix,
} from "../../001-tetris-basic/code/game-core.mjs";
import { buildActionPlan, choosePlacement } from "./ai-core.mjs";

const BLOCK = 28;
const ACTION_INTERVAL = 100;
const canvas = document.querySelector("#board");
const context = canvas.getContext("2d");
const status = document.querySelector("#status");
const pauseButton = document.querySelector("#pause");
const values = Object.fromEntries(
  ["pieces", "lines", "score", "piece", "rotation", "column", "height", "holes", "bumpiness", "evaluation"]
    .map((id) => [id, document.querySelector(`#${id}`)]),
);
const trace = document.querySelector("#trace");

let board;
let active;
let decision;
let paused;
let gameOver;
let pieces;
let lines;
let score;
let seed;
let bag;
let actions;
let lastAction;

function random() {
  seed ^= seed << 13;
  seed ^= seed >>> 17;
  seed ^= seed << 5;
  return (seed >>> 0) / 4_294_967_296;
}

function shuffledBag() {
  const kinds = Object.keys(SHAPES);
  for (let index = kinds.length - 1; index > 0; index -= 1) {
    const swap = Math.floor(random() * (index + 1));
    [kinds[index], kinds[swap]] = [kinds[swap], kinds[index]];
  }
  return kinds;
}

function takeKind() {
  if (!bag.length) bag = shuffledBag();
  return bag.pop();
}

function updateReadouts() {
  values.pieces.textContent = pieces;
  values.lines.textContent = lines;
  values.score.textContent = String(score).padStart(6, "0");
  if (!decision || !active) return;
  values.piece.textContent = active.kind;
  values.rotation.textContent = `${decision.rotation * 90}°`;
  values.column.textContent = `${decision.x + 1} of ${COLS}`;
  values.height.textContent = decision.maxHeight;
  values.holes.textContent = decision.holes;
  values.bumpiness.textContent = decision.bumpiness;
  values.evaluation.textContent = decision.score;
}

function addTrace() {
  const item = document.createElement("li");
  item.innerHTML = `<b>${String(pieces).padStart(3, "0")}</b><span>${active.kind} · col ${decision.x + 1} · ${decision.rotation * 90}°</span><em>${decision.score}</em>`;
  trace.prepend(item);
  while (trace.children.length > 7) trace.lastElementChild.remove();
}

function planPiece() {
  const kind = takeKind();
  decision = choosePlacement(board, kind);
  if (!decision) {
    gameOver = true;
    paused = true;
    status.textContent = "Stack limit reached. Restart to run the same seed again.";
    pauseButton.textContent = "Resume";
    return;
  }
  active = createPiece(kind);
  actions = buildActionPlan(active.x, decision);
  status.textContent = `Evaluated ${kind}; ${actions.length} legal inputs queued.`;
  updateReadouts();
}

function applyNextAction() {
  const action = actions.shift();
  if (!action) {
    lockPiece();
    return;
  }

  if (action === "rotate") {
    const matrix = rotateMatrix(active.matrix);
    if (collides(board, active, 0, 0, matrix)) return failPlan(action);
    active.matrix = matrix;
  } else {
    const [x, y] = action === "left" ? [-1, 0] : action === "right" ? [1, 0] : [0, 1];
    if (collides(board, active, x, y)) return failPlan(action);
    active.x += x;
    active.y += y;
  }

  status.textContent = `${active.kind}: ${action} · ${actions.length} inputs remain.`;
}

function failPlan(action) {
  gameOver = true;
  paused = true;
  status.textContent = `Plan stopped: ${action} became illegal. Restart the seed.`;
  pauseButton.textContent = "Resume";
}

function lockPiece() {
  board = merge(board, active);
  const result = clearLines(board);
  board = result.board;
  pieces += 1;
  lines += result.lines;
  score += 10 + result.lines * 1_000;
  addTrace();
  status.textContent = result.lines
    ? `Placed ${active.kind}. Cleared ${result.lines} line${result.lines === 1 ? "" : "s"}.`
    : `Placed ${active.kind}. No line clear.`;
  planPiece();
  updateReadouts();
}

function reset() {
  board = createBoard();
  active = null;
  decision = null;
  paused = false;
  gameOver = false;
  pieces = 0;
  lines = 0;
  score = 0;
  seed = 0x0df00d;
  bag = [];
  actions = [];
  lastAction = performance.now();
  trace.replaceChildren();
  pauseButton.textContent = "Pause run";
  planPiece();
  updateReadouts();
}

function togglePause() {
  if (gameOver) return;
  paused = !paused;
  pauseButton.textContent = paused ? "Resume run" : "Pause run";
  status.textContent = paused ? "Run paused." : "Run resumed.";
  lastAction = performance.now();
}

function drawCell(x, y, kind, alpha = 1) {
  context.globalAlpha = alpha;
  context.fillStyle = COLORS[kind];
  context.fillRect(x * BLOCK + 2, y * BLOCK + 2, BLOCK - 4, BLOCK - 4);
  context.fillStyle = "rgba(255,255,255,.36)";
  context.fillRect(x * BLOCK + 5, y * BLOCK + 5, BLOCK - 10, 3);
  context.globalAlpha = 1;
}

function draw() {
  context.fillStyle = "#f1eee5";
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.strokeStyle = "rgba(34, 48, 57, .09)";
  for (let x = 1; x < COLS; x += 1) {
    context.beginPath();
    context.moveTo(x * BLOCK + 0.5, 0);
    context.lineTo(x * BLOCK + 0.5, canvas.height);
    context.stroke();
  }
  for (let y = 1; y < ROWS; y += 1) {
    context.beginPath();
    context.moveTo(0, y * BLOCK + 0.5);
    context.lineTo(canvas.width, y * BLOCK + 0.5);
    context.stroke();
  }
  board.forEach((row, y) => row.forEach((kind, x) => kind && drawCell(x, y, kind)));
  if (active && !gameOver) {
    active.matrix.forEach((row, y) => row.forEach((filled, x) => {
      if (filled) {
        drawCell(active.x + x, decision.y + y, active.kind, 0.14);
        drawCell(active.x + x, active.y + y, active.kind);
      }
    }));
  }
}

function frame(timestamp) {
  if (!paused && !gameOver && active && timestamp - lastAction >= ACTION_INTERVAL) {
    applyNextAction();
    lastAction = timestamp;
  }
  draw();
  requestAnimationFrame(frame);
}

pauseButton.addEventListener("click", togglePause);
document.querySelector("#restart").addEventListener("click", reset);

reset();
requestAnimationFrame(frame);
