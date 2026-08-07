import test from "node:test";
import assert from "node:assert/strict";
import { createBoard } from "../../001-tetris-basic/code/game-core.mjs";
import { choosePlacement } from "../../002-tetris-ai/code/ai-core.mjs";
import {
  chooseRandomPlacement,
  makeRandom,
  pieceSequence,
  placementIsLegal,
  runMatch,
  summarize,
} from "./arena-core.mjs";

test("the same seed produces the same fair piece stream", () => {
  assert.deepEqual(pieceSequence(42, 30), pieceSequence(42, 30));
  assert.equal(new Set(pieceSequence(42, 7)).size, 7);
});

test("both strategies return legal placements", () => {
  const board = createBoard();
  assert.equal(placementIsLegal(board, "T", choosePlacement(board, "T")), true);
  assert.equal(
    placementIsLegal(board, "T", chooseRandomPlacement(board, "T", makeRandom(9))),
    true,
  );
});

test("a fixed match is deterministic and free of illegal moves", () => {
  assert.deepEqual(runMatch(17, 100), runMatch(17, 100));
  assert.equal(summarize([runMatch(17, 100)]).illegalMoves, 0);
});

test("the heuristic beats random placement across fixed seeds", () => {
  const result = summarize(Array.from({ length: 20 }, (_, index) => runMatch(index + 1, 200)));
  assert.ok(result.heuristicWins >= 18, JSON.stringify(result));
  assert.ok(result.heuristicLines >= result.randomLines * 3, JSON.stringify(result));
  assert.equal(result.illegalMoves, 0);
});
