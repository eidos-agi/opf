import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const artifact = JSON.parse(await readFile(new URL("./artifact.json", import.meta.url), "utf8"));

test("headline metrics reconcile to the cohort tables", () => {
  const headline = artifact.snapshot.datasets.headline[0];
  const cohorts = artifact.snapshot.datasets.cohort_summary;
  assert.equal(headline.extra_lines, cohorts[1].winner_lines - cohorts[1].comparison_lines);
  assert.equal(headline.illegal_moves, cohorts.reduce((sum, row) => sum + row.illegal_moves, 0));
  assert.equal(headline.total_matches, cohorts.reduce((sum, row) => sum + row.matches, 0));
});

test("every visible data component resolves to executable source SQL", () => {
  const source = artifact.sources.find(({ id }) => id === "cohort_pipeline");
  assert.match(source.query.sql, /^WITH evidence/);
  const sourceBacked = [
    ...artifact.manifest.cards,
    ...artifact.manifest.charts,
    ...artifact.manifest.tables,
  ];
  assert.ok(sourceBacked.every(({ sourceId }) => sourceId === source.id));
});

test("the default view carries all four maxims and all evidence forms", () => {
  const maximBlock = artifact.manifest.blocks.find(({ id }) => id === "maxims");
  assert.equal((maximBlock.body.match(/^\d\./gm) ?? []).length, 4);
  assert.equal(artifact.manifest.charts.length, 3);
  assert.equal(artifact.manifest.cards.length, 4);
  assert.equal(artifact.manifest.tables.length, 1);
});
