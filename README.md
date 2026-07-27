# Public Trend Signal MVP

[![tests](https://github.com/stomeonst/public-trend-signal-mvp/actions/workflows/tests.yml/badge.svg)](https://github.com/stomeonst/public-trend-signal-mvp/actions/workflows/tests.yml)

A local, reproducible proof of an authorized trend-data pipeline.

This repository uses fictional records. It does not scrape TikTok, Instagram, YouTube, or any other platform. It contains no customer data, credentials, cookies, private URLs, or paid API calls.

## Fixed-scope paid trial

Need a similar pipeline for an authorized export, API, or customer-owned workspace?

**Data Signal Audit: USD 150 or RMB 999.** The fixed scope covers one sanitized sample of up to 100 records, one source-to-output field map, one deduplication and scoring review, one prioritized findings report, and one written clarification. Implementation, paid APIs, production credentials, and ongoing monitoring require a separate written scope.

1. [Submit a public, sanitized request in English](https://github.com/stomeonst/launchclear-capability-samples/issues/new?template=data-signal-audit-request.yml).
2. [用中文提交公开且已脱敏的数据洞察审计需求](https://github.com/stomeonst/launchclear-capability-samples/issues/new?template=data-signal-audit-request-zh.yml)。
3. [Review the automation rescue sample](https://chris-saas-services.stomeonst123.chatgpt.site/resources/automation-rescue-sample) for a separate USD 120 or RMB 799 workflow repair scope.

Do not place credentials, API keys, personal data, customer data, private URLs, production exports, or confidential logs in a public GitHub issue. A request starts a scope review only. Work starts after scope, payment, access boundaries, and acceptance criteria are confirmed in writing.

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

## Bilingual Python review proof

[`docs/python-code-review-sample.md`](docs/python-code-review-sample.md) reviews one intentionally flawed fictional function in English and Simplified Chinese. It includes:

1. A concrete correctness defect and minimal counterexample.
2. Edge-case, validation, readability, and normalization findings.
3. Time and space complexity analysis.
4. A typed reference correction.
5. Six focused regression tests.

The fixture contains no customer code, private repository material, credentials, or production data.

## Simplified Chinese AI evaluation proof

[`docs/simplified-chinese-ai-evaluation-sample.md`](docs/simplified-chinese-ai-evaluation-sample.md) evaluates one fictional AI answer against a weighted bilingual rubric. It includes:

1. Explicit instruction following and factual support checks.
2. Mainland China language quality and localization review.
3. Severity tagged findings tied to visible evidence.
4. A bounded reference revision.
5. Second reviewer consistency checks.

The sample contains no private benchmark, customer prompt, model trace, personal data, or confidential guideline.

## English to Simplified Chinese translation evaluation proof

[`docs/english-to-simplified-chinese-translation-evaluation-sample.md`](docs/english-to-simplified-chinese-translation-evaluation-sample.md) evaluates one fictional machine translation using a public, purpose-built taxonomy. It includes:

1. A consequential negation error with source-linked evidence.
2. Accuracy, terminology, language quality, locale suitability, and completeness checks.
3. Critical, major, and minor severity definitions.
4. A corrected Simplified Chinese target.
5. Acceptance and second-review checks.

The sample contains no customer source text, private benchmark, proprietary scoring guide, model trace, personal data, or confidential terminology.

## Test

```bash
python3 -m unittest discover -s tests -v
```

The tests validate both the Python pipeline and the public n8n workflow structure, including its credential-free boundary.

## Production boundary

A customer implementation would replace the fixture reader with a customer-authorized API or export, replace the rule classifier with an approved model adapter when needed, and connect the CSV contract to a customer-owned Feishu or Notion workspace. Account access, source permissions, API costs, retention rules, and acceptance criteria must be confirmed before that work starts.
