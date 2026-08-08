# Agent Evidence Atlas

Example 005 is a source-backed analytics website for the maxims demonstrated by examples 001–004.

```bash
node examples/005-agent-evidence-atlas/code/build-data.mjs
node /Users/dshanklinbv/.codex/plugins/cache/openai-curated-remote/data-analytics/0.2.8-13ceeea1f599/skills/build-report/scripts/deliver_portable_artifact.mjs \
  --input examples/005-agent-evidence-atlas/code/artifact.json \
  --output examples/005-agent-evidence-atlas/code/index.html
python3 -m opf.validate --strict examples/005-agent-evidence-atlas/opf
```

The generated `index.html` is a self-contained read-only site: no CDN, sidecar, live service, or network request is required.
