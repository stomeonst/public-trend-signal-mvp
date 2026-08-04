# Fictional MCP to Email Fixed Scope Proof

This proof shows how a structured, MCP-shaped video analysis response can become a concise email report inside an importable n8n workflow. Every input is fictional. The workflow is inactive, contains no credentials, makes no network request, and leaves the email destination disabled for reviewer inspection.

Workflow file:

[`examples/n8n-fictional-mcp-to-email-workflow.json`](../examples/n8n-fictional-mcp-to-email-workflow.json)

## Sanitized input contract

Each fixture contains these fields:

| Field | Purpose | Validation |
| --- | --- | --- |
| `request_id` | Stable delivery and duplicate-control key | Required |
| `video_title` | Human-readable report title | Required and whitespace normalized |
| `video_url` | Source reference for the report | Must use the reserved `example.invalid` domain in this proof |
| `summary` | Main analysis result | Required |
| `confidence` | Normalized model confidence | Clamped to the range 0 to 1 |
| `highlights` | Timestamped observations | Optional array with non-empty labels |
| `recipient` | Destination for the prepared report | Must use `@example.invalid` in this proof |

The fixture includes one complete case, one repeated request ID, and one case with a missing summary.

## Expected normal path

1. `Manual Trigger` loads the three fictional MCP responses.
2. `Normalize and Validate` creates a stable schema and visible validation errors.
3. `Deduplicate by Request ID` keeps the first valid request eligible for delivery.
4. `Ready for Email?` routes only valid, non-duplicate records to report preparation.
5. `Prepare Email Report` creates a plain-text subject and body with the summary, confidence, highlights, source reference, and request ID.
6. The prepared payload reaches `Email Destination (Disabled)` for inspection without sending a message.

Expected result for `demo-request-001`: one email payload is prepared with status `email_payload_ready`.

## Expected human review path

The second `demo-request-001` record receives `duplicate_request_id`. The incomplete `demo-request-002` record receives `missing_summary`. Both records go to `Human Review Queue` with `send_email: false` and a visible list of review reasons.

This path demonstrates that a repeated execution or incomplete response does not silently produce a second report.

## Email Destination (Disabled)

The final node uses n8n's email-send node type, but it is deliberately disabled and has no credential reference. Its retry settings are visible for review: three maximum attempts with a one-second wait between attempts. The public workflow therefore proves the destination shape and retry boundary without sending an email.

## Observable acceptance checks

1. The workflow imports as valid JSON and remains inactive.
2. Node names and identifiers are unique.
3. Every connection points to an existing node.
4. Complete data follows the email path.
5. Missing summaries follow the human review path.
6. Repeated request IDs follow the human review path.
7. Only one eligible payload exists for a repeated request ID.
8. The report retains the request ID and source reference.
9. The subject and body are plain-text, visible, and deterministic.
10. The email destination stays disabled until the owner configures it.
11. The workflow contains no credential object or HTTP request node.
12. All public URLs and email addresses use the reserved `example.invalid` domain.

Run the focused verification with:

```bash
python3 -m unittest tests.test_mcp_to_email_workflow -v
```

## Fixed scope offer

The corresponding paid pilot is USD 139 for one sanitized response format, one importable n8n workflow, one email output, the 12 checks above, a concise handoff, and one bounded retest. Delivery is within 48 hours after the sanitized fixture, expected email layout, written scope, lawful payment path, and payment are confirmed.

## Production boundary

A live implementation would replace the fictional fixture with a customer-authorized response or connection and would replace the disabled email placeholder with a customer-owned credential. Live MCP authentication, production credentials, production deployment, permission or ownership decisions, customer data, security testing, legal review, and ongoing maintenance require separate owner decisions and written scope.

This repository does not claim a customer engagement, live deployment, or commercial result. It provides directly inspectable evidence of the workflow structure and acceptance logic.
