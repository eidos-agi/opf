import {
  clearLines,
  collides,
  createPiece,
  dropDistance,
  merge,
  rotateMatrix,
} from "../../001-tetris-basic/code/game-core.mjs";

export function uniqueRotations(matrix) {
  const rotations = [];
  let current = matrix.map((row) => [...row]);
  for (let turn = 0; turn < 4; turn += 1) {
    const key = JSON.stringify(current);
    if (!rotations.some((entry) => entry.key === key)) {
      rotations.push({ key, matrix: current, rotation: turn });
    }
    current = rotateMatrix(current);
  }
  return rotations;
}

export function boardMetrics(board) {
  const heights = Array(board[0].length).fill(0);
  let holes = 0;

  for (let x = 0; x < board[0].length; x += 1) {
    let seenBlock = false;
    for (let y = 0; y < board.length; y += 1) {
      if (board[y][x]) {
        if (!seenBlock) heights[x] = board.length - y;
        seenBlock = true;
      } else if (seenBlock) {
        holes += 1;
      }
    }
  }

  return {
    heights,
    aggregateHeight: heights.reduce((sum, height) => sum + height, 0),
    maxHeight: Math.max(...heights),
    holes,
    bumpiness: heights.slice(1).reduce(
      (sum, height, index) => sum + Math.abs(height - heights[index]),
      0,
    ),
  };
}

export function scoreBoard(board, linesCleared = 0) {
  const metrics = boardMetrics(board);
  const score =
    linesCleared * 1_000 -
    metrics.aggregateHeight * 8 -
    metrics.holes * 45 -
    metrics.bumpiness * 6 -
    metrics.maxHeight * 4;
  return { ...metrics, score, linesCleared };
}

export function legalPlacements(board, kind) {
  const piece = createPiece(kind, board[0].length);
  const placements = [];

  for (const rotation of uniqueRotations(piece.matrix)) {
    for (let x = -rotation.matrix[0].length + 1; x < board[0].length; x += 1) {
      const candidate = { kind, matrix: rotation.matrix, x, y: 0 };
      if (collides(board, candidate)) continue;
      candidate.y = dropDistance(board, candidate);
      const cleared = clearLines(merge(board, candidate));
      placements.push({
        x,
        y: candidate.y,
        rotation: rotation.rotation,
        matrix: rotation.matrix,
        board: cleared.board,
        ...scoreBoard(cleared.board, cleared.lines),
      });
    }
  }

  return placements;
}

export function choosePlacement(board, kind) {
  const center = (board[0].length - 1) / 2;
  return legalPlacements(board, kind).sort((a, b) =>
    b.score - a.score ||
    b.linesCleared - a.linesCleared ||
    a.holes - b.holes ||
    a.aggregateHeight - b.aggregateHeight ||
    Math.abs(a.x - center) - Math.abs(b.x - center) ||
    a.rotation - b.rotation ||
    a.x - b.x,
  )[0] ?? null;
}

export function buildActionPlan(startX, placement) {
  const horizontal = placement.x - startX;
  return [
    ...Array(placement.rotation).fill("rotate"),
    ...Array(Math.abs(horizontal)).fill(horizontal < 0 ? "left" : "right"),
    ...Array(placement.y).fill("down"),
  ];
}
