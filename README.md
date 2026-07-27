# Public Trend Signal MVP

[![tests](https://github.com/stomeonst/public-trend-signal-mvp/actions/workflows/tests.yml/badge.svg)](https://github.com/stomeonst/public-trend-signal-mvp/actions/workflows/tests.yml)

A local, reproducible proof of an authorized trend-data pipeline.

This repository uses fictional records. It does not scrape TikTok, Instagram, YouTube, or any other platform. It contains no customer data, credentials, cookies, private URLs, or paid API calls.

## What it proves

1. Normalize records from more than one source shape.
2. Deduplicate repeated URLs and near-identical titles.
3. Rank recent public signals with a deterministic score.
4. Classify records using an explicit, replaceable ruleset.
5. Route weak or invalid results to human review.
6. Export a Feishu Bitable or Notion compatible CSV.
7. Produce a run receipt with counts and SHA-256 hashes.

## Run

```bash
python3 -m trend_signal.cli \
  --input examples/fictional_signals.jsonl \
  --output-dir build
```

Outputs:

* `build/signals.csv`
* `build/review.csv`
* `build/errors.jsonl`
* `build/run-receipt.json`

## Importable n8n proof

`examples/n8n-public-trend-signal-workflow.json` is an importable concept workflow that demonstrates the same bounded pipeline inside n8n:

1. Start manually with five fictional records.
2. Normalize titles and remove tracking parameters from URLs.
3. Deduplicate records with a stable source and URL key.
4. Apply a deterministic trend score.
5. Split low-confidence records into a human review queue.
6. Prepare accepted records for a customer-owned table connector.

The workflow intentionally has no credentials, external requests, customer data, production URLs, or automatic publishing nodes. The final table connector remains outside the public sample because workspace access and destination schema require customer authorization.

## Test

```bash
python3 -m unittest discover -s tests -v
```

The tests validate both the Python pipeline and the public n8n workflow structure, including its credential-free boundary.

## Production boundary

A customer implementation would replace the fixture reader with a customer-authorized API or export, replace the rule classifier with an approved model adapter when needed, and connect the CSV contract to a customer-owned Feishu or Notion workspace. Account access, source permissions, API costs, retention rules, and acceptance criteria must be confirmed before that work starts.
