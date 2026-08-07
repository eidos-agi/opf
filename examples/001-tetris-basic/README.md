# Basic Tetris — OPF dogfood

The product definition lives in `opf/`; the implementation lives in `app/`.

```bash
python3 -m opf.validate --strict examples/001-tetris-basic/opf
node --test examples/001-tetris-basic/code/game-core.test.mjs
python3 -m http.server 8789 --directory examples/001-tetris-basic/code
```

Open <http://127.0.0.1:8789> to play.
