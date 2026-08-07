export const COLS = 10;
export const ROWS = 20;

export const SHAPES = {
  I: [[1, 1, 1, 1]],
  J: [[1, 0, 0], [1, 1, 1]],
  L: [[0, 0, 1], [1, 1, 1]],
  O: [[1, 1], [1, 1]],
  S: [[0, 1, 1], [1, 1, 0]],
  T: [[0, 1, 0], [1, 1, 1]],
  Z: [[1, 1, 0], [0, 1, 1]],
};

export const COLORS = {
  I: "#315efb",
  J: "#6f5bd3",
  L: "#ff8b3d",
  O: "#ffca3a",
  S: "#43c59e",
  T: "#d95dcb",
  Z: "#ff5a5f",
};

export function createBoard(rows = ROWS, cols = COLS) {
  return Array.from({ length: rows }, () => Array(cols).fill(null));
}

export function createPiece(kind, cols = COLS) {
  const matrix = SHAPES[kind].map((row) => [...row]);
  return {
    kind,
    matrix,
    x: Math.floor((cols - matrix[0].length) / 2),
    y: 0,
  };
}

export function rotateMatrix(matrix) {
  return matrix[0].map((_, column) => matrix.map((row) => row[column]).reverse());
}

export function collides(board, piece, offsetX = 0, offsetY = 0, matrix = piece.matrix) {
  for (let y = 0; y < matrix.length; y += 1) {
    for (let x = 0; x < matrix[y].length; x += 1) {
      if (!matrix[y][x]) continue;
      const boardX = piece.x + x + offsetX;
      const boardY = piece.y + y + offsetY;
      if (boardX < 0 || boardX >= board[0].length || boardY >= board.length) return true;
      if (boardY >= 0 && board[boardY][boardX]) return true;
    }
  }
  return false;
}

export function merge(board, piece) {
  const merged = board.map((row) => [...row]);
  piece.matrix.forEach((row, y) => {
    row.forEach((filled, x) => {
      const boardY = piece.y + y;
      if (filled && boardY >= 0) merged[boardY][piece.x + x] = piece.kind;
    });
  });
  return merged;
}

export function clearLines(board) {
  const remaining = board.filter((row) => row.some((cell) => !cell));
  const lines = board.length - remaining.length;
  const empty = Array.from({ length: lines }, () => Array(board[0].length).fill(null));
  return { board: [...empty, ...remaining], lines };
}

export function dropDistance(board, piece) {
  let distance = 0;
  while (!collides(board, piece, 0, distance + 1)) distance += 1;
  return distance;
}
