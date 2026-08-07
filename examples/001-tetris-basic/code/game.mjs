import {
  COLORS,
  COLS,
  ROWS,
  SHAPES,
  clearLines,
  collides,
  createBoard,
  createPiece,
  dropDistance,
  merge,
  rotateMatrix,
} from "./game-core.mjs";

const BLOCK = 30;
const SCORE_BY_LINES = [0, 100, 300, 500, 800];
const boardCanvas = document.querySelector("#board");
const boardContext = boardCanvas.getContext("2d");
const nextCanvas = document.querySelector("#next");
const nextContext = nextCanvas.getContext("2d");
const scoreElement = document.querySelector("#score");
const linesElement = document.querySelector("#lines");
const levelElement = document.querySelector("#level");
const liveStatus = document.querySelector("#live-status");
const overlay = document.querySelector("#status-overlay");
const overlayTitle = document.querySelector("#overlay-title");
const overlayCopy = document.querySelector("#overlay-copy");

let board;
let active;
let next;
let bag;
let score;
let lines;
let level;
let gameOver;
let paused;
let lastDrop;

function shuffledBag() {
  const kinds = Object.keys(SHAPES);
  for (let i = kinds.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [kinds[i], kinds[j]] = [kinds[j], kinds[i]];
  }
  return kinds;
}

function takePiece() {
  if (!bag.length) bag = shuffledBag();
  return createPiece(bag.pop());
}

function updateReadouts() {
  scoreElement.textContent = String(score).padStart(6, "0");
  linesElement.textContent = lines;
  levelElement.textContent = level;
}

function announce(message) {
  liveStatus.textContent = message;
}

function showOverlay(title, copy) {
  overlayTitle.textContent = title;
  overlayCopy.textContent = copy;
  overlay.hidden = false;
}

function hideOverlay() {
  overlay.hidden = true;
}

function spawnPiece() {
  active = next ?? takePiece();
  next = takePiece();
  if (collides(board, active)) {
    gameOver = true;
    showOverlay("Game over", "Press R or choose Restart game");
    announce(`Game over. Final score ${score}.`);
  }
}

function resetGame() {
  board = createBoard();
  bag = shuffledBag();
  active = null;
  next = null;
  score = 0;
  lines = 0;
  level = 1;
  gameOver = false;
  paused = false;
  lastDrop = performance.now();
  hideOverlay();
  spawnPiece();
  updateReadouts();
  announce("New game started.");
  boardCanvas.focus();
}

function lockPiece() {
  board = merge(board, active);
  const result = clearLines(board);
  board = result.board;
  if (result.lines) {
    lines += result.lines;
    score += SCORE_BY_LINES[result.lines] * level;
    level = Math.floor(lines / 10) + 1;
    announce(`${result.lines} line${result.lines === 1 ? "" : "s"} cleared.`);
  }
  spawnPiece();
  updateReadouts();
}

function move(horizontal, vertical) {
  if (gameOver || paused) return;
  if (!collides(board, active, horizontal, vertical)) {
    active.x += horizontal;
    active.y += vertical;
    return;
  }
  if (vertical > 0) lockPiece();
}

function rotate() {
  if (gameOver || paused) return;
  const rotated = rotateMatrix(active.matrix);
  for (const kick of [0, -1, 1, -2, 2]) {
    if (!collides(board, active, kick, 0, rotated)) {
      active.matrix = rotated;
      active.x += kick;
      return;
    }
  }
}

function softDrop() {
  if (gameOver || paused) return;
  if (!collides(board, active, 0, 1)) {
    active.y += 1;
    score += 1;
    updateReadouts();
  } else {
    lockPiece();
  }
  lastDrop = performance.now();
}

function hardDrop() {
  if (gameOver || paused) return;
  const distance = dropDistance(board, active);
  active.y += distance;
  score += distance * 2;
  lockPiece();
  lastDrop = performance.now();
}

function togglePause() {
  if (gameOver) return;
  paused = !paused;
  if (paused) {
    showOverlay("Paused", "Press P or choose Pause to continue");
    announce("Game paused.");
  } else {
    hideOverlay();
    lastDrop = performance.now();
    announce("Game resumed.");
  }
}

function runAction(action) {
  const actions = {
    left: () => move(-1, 0),
    right: () => move(1, 0),
    down: softDrop,
    rotate,
    drop: hardDrop,
    pause: togglePause,
  };
  actions[action]?.();
}

function drawCell(context, x, y, color, size = BLOCK, alpha = 1) {
  context.globalAlpha = alpha;
  context.fillStyle = color;
  context.fillRect(x * size + 1, y * size + 1, size - 2, size - 2);
  context.fillStyle = "rgba(255,255,255,0.28)";
  context.fillRect(x * size + 3, y * size + 3, size - 6, 4);
  context.strokeStyle = "rgba(19,33,60,0.35)";
  context.strokeRect(x * size + 1.5, y * size + 1.5, size - 3, size - 3);
  context.globalAlpha = 1;
}

function drawMatrix(context, matrix, offsetX, offsetY, kind, size = BLOCK, alpha = 1) {
  matrix.forEach((row, y) => {
    row.forEach((filled, x) => {
      if (filled && offsetY + y >= 0) {
        drawCell(context, offsetX + x, offsetY + y, COLORS[kind], size, alpha);
      }
    });
  });
}

function drawGrid() {
  boardContext.fillStyle = "#f7f9fc";
  boardContext.fillRect(0, 0, boardCanvas.width, boardCanvas.height);
  boardContext.strokeStyle = "rgba(19,33,60,0.08)";
  boardContext.lineWidth = 1;
  for (let x = 1; x < COLS; x += 1) {
    boardContext.beginPath();
    boardContext.moveTo(x * BLOCK + 0.5, 0);
    boardContext.lineTo(x * BLOCK + 0.5, ROWS * BLOCK);
    boardContext.stroke();
  }
  for (let y = 1; y < ROWS; y += 1) {
    boardContext.beginPath();
    boardContext.moveTo(0, y * BLOCK + 0.5);
    boardContext.lineTo(COLS * BLOCK, y * BLOCK + 0.5);
    boardContext.stroke();
  }
}

function drawNext() {
  nextContext.clearRect(0, 0, nextCanvas.width, nextCanvas.height);
  if (!next) return;
  const size = 22;
  const width = next.matrix[0].length * size;
  const height = next.matrix.length * size;
  const x = (nextCanvas.width - width) / (2 * size);
  const y = (nextCanvas.height - height) / (2 * size);
  drawMatrix(nextContext, next.matrix, x, y, next.kind, size);
}

function draw() {
  drawGrid();
  board.forEach((row, y) => {
    row.forEach((kind, x) => {
      if (kind) drawCell(boardContext, x, y, COLORS[kind]);
    });
  });
  if (active && !gameOver) {
    const ghostY = active.y + dropDistance(board, active);
    drawMatrix(boardContext, active.matrix, active.x, ghostY, active.kind, BLOCK, 0.18);
    drawMatrix(boardContext, active.matrix, active.x, active.y, active.kind);
  }
  drawNext();
}

function frame(timestamp) {
  const interval = Math.max(100, 850 - (level - 1) * 70);
  if (!gameOver && !paused && timestamp - lastDrop >= interval) {
    move(0, 1);
    lastDrop = timestamp;
  }
  draw();
  requestAnimationFrame(frame);
}

const keyActions = {
  ArrowLeft: "left",
  ArrowRight: "right",
  ArrowDown: "down",
  ArrowUp: "rotate",
  x: "rotate",
  X: "rotate",
  " ": "drop",
  p: "pause",
  P: "pause",
};

document.addEventListener("keydown", (event) => {
  if (event.key === "r" || event.key === "R") {
    resetGame();
    return;
  }
  const action = keyActions[event.key];
  if (!action) return;
  event.preventDefault();
  runAction(action);
});

document.querySelector("#restart").addEventListener("click", resetGame);
document.querySelectorAll("[data-action]").forEach((button) => {
  button.addEventListener("click", () => runAction(button.dataset.action));
});

resetGame();
requestAnimationFrame(frame);
