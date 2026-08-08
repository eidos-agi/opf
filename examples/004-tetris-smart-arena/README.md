# Tetris Smart Arena

Example 004 compares two competent agents. The depth-one expert uses example 002's board heuristic. The depth-two expert evaluates the best reply for the known next piece before choosing.

```bash
python3 -m http.server 8000
# open http://127.0.0.1:8000/examples/004-tetris-smart-arena/code/

node --test examples/004-tetris-smart-arena/code/smart-core.test.mjs
node examples/004-tetris-smart-arena/code/evaluate.mjs 50 300
python3 -m opf.validate --strict examples/004-tetris-smart-arena/opf
```

Both agents receive the same seeded seven-bag stream and play through at most one ordinary input per 100 ms. The live reason panel exposes current-piece score, next-piece score, searched replies, and choice divergences.
