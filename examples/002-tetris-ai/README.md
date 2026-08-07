# Tetris AI — OPF dogfood 002

This example reuses 001's game engine and adds a deterministic search-and-heuristic placement agent. The product definition lives in `opf/`; the implementation lives in `code/`.

```bash
python3 -m opf.validate --strict examples/002-tetris-ai/opf
node --test examples/002-tetris-ai/code/ai-core.test.mjs
python3 -m http.server 8789 --directory examples
```

Open <http://127.0.0.1:8789/002-tetris-ai/code/> to watch the agent play.

The agent evaluates every legal rotation and column using line clears, aggregate height, holes, maximum height, and bumpiness. It then reaches the chosen landing through normal game inputs, limited to one nudge or rotation every 100 ms. It does not call a model or network service.
