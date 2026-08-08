import { clearLines, createBoard, merge } from "../../001-tetris-basic/code/game-core.mjs";
import { choosePlacement, legalPlacements } from "../../002-tetris-ai/code/ai-core.mjs";
import { pieceSequence, placementIsLegal } from "../../003-tetris-ai-arena/code/arena-core.mjs";

export function chooseLookaheadPlacement(board, kind, nextKind) {
  const candidates = legalPlacements(board, kind).map((placement) => {
    const replies = nextKind ? legalPlacements(placement.board, nextKind) : [];
    const futureScore = replies.length
      ? Math.max(...replies.map((reply) => reply.score))
      : placement.score;
    return {
      ...placement,
      immediateScore: placement.score,
      futureScore,
      combinedScore: placement.score + futureScore,
      replies: replies.length,
    };
  });
  return candidates.sort((a, b) =>
    b.combinedScore - a.combinedScore ||
    b.futureScore - a.futureScore ||
    b.immediateScore - a.immediateScore ||
    a.rotation - b.rotation ||
    a.x - b.x,
  )[0] ?? null;
}

export function futureScoreFor(placement, nextKind) {
  const replies = nextKind ? legalPlacements(placement.board, nextKind) : [];
  return replies.length ? Math.max(...replies.map((reply) => reply.score)) : placement.score;
}

export function chooseGreedyPlacement(board, kind) {
  const placement = choosePlacement(board, kind);
  return placement ? {
    ...placement,
    immediateScore: placement.score,
    futureScore: null,
    combinedScore: placement.score,
    replies: 0,
  } : null;
}

export function simulateSmart({ sequence, choose }) {
  let board = createBoard();
  let pieces = 0;
  let lines = 0;
  let illegalMoves = 0;
  for (let index = 0; index < sequence.length; index += 1) {
    const kind = sequence[index];
    const placement = choose(board, kind, sequence[index + 1]);
    if (!placement) break;
    if (!placementIsLegal(board, kind, placement)) {
      illegalMoves += 1;
      break;
    }
    const result = clearLines(merge(board, { kind, ...placement }));
    board = result.board;
    pieces += 1;
    lines += result.lines;
  }
  return { pieces, lines, illegalMoves };
}

export function runSmartMatch(seed, pieceLimit = 300) {
  const sequence = pieceSequence(seed, pieceLimit);
  return {
    seed,
    greedy: simulateSmart({ sequence, choose: chooseGreedyPlacement }),
    lookahead: simulateSmart({ sequence, choose: chooseLookaheadPlacement }),
  };
}

export function summarizeSmart(matches) {
  const total = (side, field) => matches.reduce((sum, match) => sum + match[side][field], 0);
  return {
    matches: matches.length,
    lookaheadWins: matches.filter((match) => match.lookahead.lines > match.greedy.lines).length,
    greedyWins: matches.filter((match) => match.greedy.lines > match.lookahead.lines).length,
    draws: matches.filter((match) => match.greedy.lines === match.lookahead.lines).length,
    greedyLines: total("greedy", "lines"),
    lookaheadLines: total("lookahead", "lines"),
    greedyPieces: total("greedy", "pieces"),
    lookaheadPieces: total("lookahead", "pieces"),
    illegalMoves: total("greedy", "illegalMoves") + total("lookahead", "illegalMoves"),
  };
}
