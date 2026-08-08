import test from "node:test";
import assert from "node:assert/strict";
import { clearLines, createBoard, merge } from "../../001-tetris-basic/code/game-core.mjs";
import { pieceSequence } from "../../003-tetris-ai-arena/code/arena-core.mjs";
import {
  chooseGreedyPlacement,
  chooseLookaheadPlacement,
  futureScoreFor,
  runSmartMatch,
  summarizeSmart,
} from "./smart-core.mjs";

test("lookahead score includes the best reply for the known next piece", () => {
  const board = createBoard();
  const choice = chooseLookaheadPlacement(board, "T", "I");
  assert.equal(choice.futureScore, futureScoreFor(choice, "I"));
  assert.equal(choice.combinedScore, choice.immediateScore + choice.futureScore);
  assert.ok(choice.replies > 0);
});

test("foresight changes at least one choice on a fixed stream", () => {
  const sequence = pieceSequence(404, 80);
  let board = createBoard();
  let divergences = 0;
  for (let index = 0; index < sequence.length; index += 1) {
    const greedy = chooseGreedyPlacement(board, sequence[index]);
    const lookahead = chooseLookaheadPlacement(board, sequence[index], sequence[index + 1]);
    if (!lookahead) break;
    if (greedy.x !== lookahead.x || greedy.rotation !== lookahead.rotation) divergences += 1;
    const result = clearLines(merge(board, { kind: sequence[index], ...lookahead }));
    board = result.board;
  }
  assert.ok(divergences > 0);
});

test("fixed matches are deterministic and legal", () => {
  assert.deepEqual(runSmartMatch(4, 100), runSmartMatch(4, 100));
  assert.equal(summarizeSmart([runSmartMatch(4, 100)]).illegalMoves, 0);
});

test("lookahead beats greedy across the declared fixed cohort", () => {
  const result = summarizeSmart(Array.from({ length: 50 }, (_, index) => runSmartMatch(index + 1, 300)));
  assert.ok(result.lookaheadWins >= 30, JSON.stringify(result));
  assert.ok(result.lookaheadLines >= result.greedyLines + 150, JSON.stringify(result));
  assert.ok(result.lookaheadPieces > result.greedyPieces, JSON.stringify(result));
  assert.equal(result.illegalMoves, 0);
});
