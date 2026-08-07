import test from "node:test";
import assert from "node:assert/strict";
import { clearLines, createBoard, merge } from "../../001-tetris-basic/code/game-core.mjs";
import { boardMetrics, buildActionPlan, choosePlacement, legalPlacements } from "./ai-core.mjs";

test("board metrics distinguish height, holes, and bumpiness", () => {
  const board = createBoard(4, 4);
  board[1][0] = "T";
  board[3][0] = "T";
  board[3][1] = "T";
  assert.deepEqual(boardMetrics(board), {
    heights: [3, 1, 0, 0],
    aggregateHeight: 4,
    maxHeight: 3,
    holes: 1,
    bumpiness: 3,
  });
});

test("every enumerated placement is legal and lands inside the board", () => {
  const board = createBoard();
  const placements = legalPlacements(board, "T");
  assert.ok(placements.length > 0);
  assert.ok(placements.every(({ board: result }) => result.length === 20 && result[0].length === 10));
});

test("the agent prefers the available line clear", () => {
  const board = createBoard();
  for (let x = 4; x < 10; x += 1) board[19][x] = "Z";
  const decision = choosePlacement(board, "I");
  assert.equal(decision.linesCleared, 1);
  assert.equal(decision.rotation, 0);
  assert.equal(decision.x, 0);
});

test("the same board and piece produce the same decision", () => {
  const board = createBoard();
  assert.deepEqual(choosePlacement(board, "L"), choosePlacement(board, "L"));
});

test("the action plan reaches a placement without teleporting", () => {
  assert.deepEqual(buildActionPlan(4, { rotation: 2, x: 1, y: 3 }), [
    "rotate", "rotate", "left", "left", "left", "down", "down", "down",
  ]);
});

test("the autonomous loop places repeatedly and clears lines", () => {
  let board = createBoard();
  let placed = 0;
  let lines = 0;
  for (const kind of "IJLOSTZ".repeat(20)) {
    const decision = choosePlacement(board, kind);
    if (!decision) break;
    const result = clearLines(merge(board, {
      kind,
      matrix: decision.matrix,
      x: decision.x,
      y: decision.y,
    }));
    board = result.board;
    placed += 1;
    lines += result.lines;
  }
  assert.ok(placed > 20);
  assert.ok(lines > 0);
});
