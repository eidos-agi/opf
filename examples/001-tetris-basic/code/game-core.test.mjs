import assert from "node:assert/strict";
import test from "node:test";

import {
  clearLines,
  collides,
  createBoard,
  createPiece,
  dropDistance,
  merge,
  rotateMatrix,
} from "./game-core.mjs";

test("rotation turns a horizontal I piece vertical", () => {
  assert.deepEqual(rotateMatrix([[1, 1, 1, 1]]), [[1], [1], [1], [1]]);
});

test("collision catches walls and settled cells", () => {
  const board = createBoard();
  const piece = createPiece("O");
  piece.x = -1;
  assert.equal(collides(board, piece), true);
  piece.x = 4;
  board[1][4] = "T";
  assert.equal(collides(board, piece), true);
});

test("merge and clear remove a complete row", () => {
  const board = createBoard(2, 4);
  board[1] = ["I", "I", null, null];
  const piece = { kind: "O", matrix: [[1, 1]], x: 2, y: 1 };
  const result = clearLines(merge(board, piece));
  assert.equal(result.lines, 1);
  assert.deepEqual(result.board[0], [null, null, null, null]);
});

test("drop distance stops on the floor", () => {
  const board = createBoard();
  const piece = createPiece("O");
  assert.equal(dropDistance(board, piece), 18);
});
