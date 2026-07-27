# China Story Trend Workflow Proof Map

Prepared on 27 July 2026 for a public, project-specific capability review.

This document maps a proposed short-video trend workflow to evidence already available in this repository. It is a self-initiated demonstration. It does not represent a customer engagement, production deployment, or live collection from TikTok, Instagram, or YouTube.

## Proposed first-stage outcome

Build one authorized source-to-table MVP that runs once per day and produces a reviewable topic brief about China-related public content.

The bounded flow is:

1. Read records from one customer-authorized API or export.
2. Normalize source fields into one contract.
3. Remove tracking parameters and block duplicates.
4. score recency and engagement signals with visible rules.
5. classify the topic and generate a concise editorial rationale.
6. route weak or invalid records to human review.
7. write approved fields to one customer-owned Feishu Bitable or Notion database.
8. retain a run receipt, error list, and maintenance checklist.

## Requirement-to-evidence map

| Project requirement | Evidence available now | Acceptance check | Remaining production proof |
| --- | --- | --- | --- |
| Make or n8n workflow | Importable n8n workflow in `examples/n8n-public-trend-signal-workflow.json` | Workflow imports without credentials and exposes each transformation step | Configure the approved runtime and customer-owned credentials |
| JSON and webhook-style field handling | Python normalization pipeline and five fictional input records | Different source shapes resolve to one documented output contract | Map the selected commercial API response |
| Filtering and deduplication | URL cleanup, stable keys, duplicate blocking, and tests | Repeated records do not appear twice in accepted output | Validate pagination and source-specific identifiers |
| Trend ranking | Deterministic score with explicit inputs | Re-running the same input produces the same ordering and receipt | Agree on source metrics and business weights |
| AI classification and editorial rationale | Explicit category contract and human-review boundary | Every accepted record has a category, evidence fields, and review status | Connect the approved model and test the customer's editorial rubric |
| Feishu or Notion output | Compatible CSV contract and connector-ready n8n output | Required columns open cleanly and preserve UTF-8 Chinese text | Connect one customer-owned destination with minimum permission |
| Failure handling | Error output, review queue, and SHA-256 run receipt | Invalid records are visible and do not silently enter accepted output | Add API retry, rate-limit, and alert rules for the chosen source |
| Maintenance handoff | Reproducible commands, tests, and production boundary | A second operator can run the fixture and inspect outputs | Document customer environment, costs, ownership, and escalation path |

## Suggested acceptance criteria

The first stage can be accepted when all of the following are true:

1. One approved source completes a scheduled run using a customer-owned account.
2. Required fields are present for at least 95 percent of valid source records.
3. Exact duplicate records do not appear in the accepted table.
4. Weak, incomplete, or invalid records enter a visible review or error queue.
5. Each accepted topic contains a source URL, publication time, category, score inputs, concise rationale, and review status.
6. The destination contains no fields outside the written schema.
7. A failed test run cannot overwrite the last accepted output.
8. One post-deployment retest passes using a sanitized sample agreed by both parties.

## Delivery and access boundaries

The fixed first stage covers one platform or one commercial data source, up to three topic groups, one daily run, one destination, one acceptance checklist, and one retest.

The customer must confirm source authorization, provide third-party accounts, and cover API, model, proxy, Feishu, or Notion charges. No private cookies, bypass methods, personal account sessions, or confidential user data should be supplied. Production access should use the minimum permissions needed for the written scope.

## Evidence links

* Repository overview: <https://github.com/stomeonst/public-trend-signal-mvp>
* Importable n8n workflow: <https://github.com/stomeonst/public-trend-signal-mvp/blob/main/examples/n8n-public-trend-signal-workflow.json>
* Automated tests: <https://github.com/stomeonst/public-trend-signal-mvp/actions/workflows/tests.yml>
