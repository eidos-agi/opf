import { clearLines, collides, createBoard, createPiece, dropDistance, merge } from "../../001-tetris-basic/code/game-core.mjs";
import { choosePlacement, legalPlacements } from "../../002-tetris-ai/code/ai-core.mjs";

export function makeRandom(seed) {
  let state = seed >>> 0;
  return () => {
    state ^= state << 13;
    state ^= state >>> 17;
    state ^= state << 5;
    return (state >>> 0) / 4_294_967_296;
  };
}

export function pieceSequence(seed, count) {
  const random = makeRandom(seed);
  const kinds = "IJLOSTZ".split("");
  const sequence = [];
  while (sequence.length < count) {
    const bag = [...kinds];
    for (let index = bag.length - 1; index > 0; index -= 1) {
      const swap = Math.floor(random() * (index + 1));
      [bag[index], bag[swap]] = [bag[swap], bag[index]];
    }
    sequence.push(...bag);
  }
  return sequence.slice(0, count);
}

export function chooseRandomPlacement(board, kind, random) {
  const placements = legalPlacements(board, kind);
  return placements[Math.floor(random() * placements.length)] ?? null;
}

export function placementIsLegal(board, kind, placement) {
  if (!placement) return false;
  const piece = createPiece(kind, board[0].length);
  piece.matrix = placement.matrix;
  piece.x = placement.x;
  piece.y = 0;
  if (collides(board, piece)) return false;
  return placement.y === dropDistance(board, piece);
}

export function applyPlacement(board, kind, placement) {
  if (!placementIsLegal(board, kind, placement)) throw new Error("illegal placement");
  const result = clearLines(merge(board, { kind, ...placement }));
  return { board: result.board, lines: result.lines };
}

export function simulate({ sequence, choose, random = () => 0 }) {
  let board = createBoard();
  let pieces = 0;
  let lines = 0;
  let illegalMoves = 0;
  for (const kind of sequence) {
    const placement = choose(board, kind, random);
    if (!placement) break;
    if (!placementIsLegal(board, kind, placement)) {
      illegalMoves += 1;
      break;
    }
    const result = applyPlacement(board, kind, placement);
    board = result.board;
    pieces += 1;
    lines += result.lines;
  }
  return { pieces, lines, illegalMoves };
}

export function runMatch(seed, pieceLimit = 300) {
  const sequence = pieceSequence(seed, pieceLimit);
  return {
    seed,
    random: simulate({
      sequence,
      choose: chooseRandomPlacement,
      random: makeRandom(seed ^ 0x9e3779b9),
    }),
    heuristic: simulate({ sequence, choose: choosePlacement }),
  };
}

export function summarize(matches) {
  const total = (side, field) => matches.reduce((sum, match) => sum + match[side][field], 0);
  const wins = matches.filter((match) => match.heuristic.lines > match.random.lines).length;
  return {
    matches: matches.length,
    heuristicWins: wins,
    randomLines: total("random", "lines"),
    heuristicLines: total("heuristic", "lines"),
    illegalMoves: total("random", "illegalMoves") + total("heuristic", "illegalMoves"),
  };
}
