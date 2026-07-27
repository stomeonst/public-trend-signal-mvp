# Public Trend Signal MVP

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

## Test

```bash
python3 -m unittest discover -s tests -v
```

## Production boundary

A customer implementation would replace the fixture reader with a customer-authorized API or export, replace the rule classifier with an approved model adapter when needed, and connect the CSV contract to a customer-owned Feishu or Notion workspace. Account access, source permissions, API costs, retention rules, and acceptance criteria must be confirmed before that work starts.
