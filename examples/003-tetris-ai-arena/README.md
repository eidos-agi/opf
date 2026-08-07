# Tetris AI Arena

Example 003 asks a product question that needs comparative evidence: does the heuristic from example 002 outperform a legal random baseline?

```bash
python3 -m http.server 8000
# open http://127.0.0.1:8000/examples/003-tetris-ai-arena/code/

node --test examples/003-tetris-ai-arena/code/arena-core.test.mjs
node examples/003-tetris-ai-arena/code/evaluate.mjs 50 300
python3 -m opf.validate --strict examples/003-tetris-ai-arena/opf
```

Both visible agents receive the same fixed seven-bag stream and may perform at most one ordinary game input every 100 ms. The evaluator uses the same strategies and seeded streams without waiting for animation.
