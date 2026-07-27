# English to Simplified Chinese Machine Translation Evaluation Sample

## Scope and evidence boundary

This is a fictional public demonstration of a reproducible translation evaluation method. It contains no customer text, private benchmark, proprietary scoring guide, model trace, personal data, or confidential terminology.

The example evaluates one English source sentence and one Simplified Chinese machine translation. The taxonomy is purpose-built for this public sample. It does not claim to reproduce a customer's private rubric.

## Fictional source

> Before issuing a refund, confirm that the payment settled successfully, the order has not already been refunded, and the customer request matches the order record.

## Candidate machine translation

> 在发出退款之前，请确认付款已成功结算，订单已经退款，并且客户请求与订单记录相匹配。

## Reference translation

> 发起退款前，请确认款项已成功入账、订单尚未退款，并核对客户的退款请求是否与订单记录一致。

## Evaluation taxonomy

| Category | Severity | Decision rule |
| --- | --- | --- |
| Accuracy | Critical, major, or minor | The target must preserve the source meaning, including negation, conditions, actors, and relationships |
| Terminology | Major or minor | Operational terms must be accurate and consistent in the stated context |
| Language quality | Major or minor | The target must use natural Simplified Chinese grammar, punctuation, and register |
| Locale suitability | Major or minor | Wording must be understandable to a Mainland China business operator without adding unsupported local assumptions |
| Completeness | Critical, major, or minor | No material source instruction may be omitted or added |

Severity meanings:

1. **Critical:** The error can reverse a consequential action or make the target unsafe to use.
2. **Major:** The error materially changes meaning or prevents reliable task completion.
3. **Minor:** The meaning remains usable, but wording, consistency, or fluency should be corrected.

## Segment review

### Decision

**Reject and revise.**

The candidate contains one critical accuracy error. It translates “has not already been refunded” as “已经退款,” which removes the negation and reverses the required precondition. A workflow operator following the candidate could issue a duplicate refund.

### Findings

| Source span | Candidate span | Category | Severity | Evidence and correction |
| --- | --- | --- | --- | --- |
| has not already been refunded | 已经退款 | Accuracy | Critical | Negation is lost and the condition is reversed. Use “尚未退款” or “未曾退款” |
| Before issuing a refund | 在发出退款之前 | Terminology | Minor | Understandable, but “发起退款前” is more natural for an operational workflow |
| the customer request matches the order record | 客户请求与订单记录相匹配 | Language quality | Minor | Grammatically valid. Adding “核对” and specifying “退款请求” improves operational clarity without changing the source |

## Corrected target

> 发起退款前，请确认款项已成功入账、订单尚未退款，并核对客户的退款请求是否与订单记录一致。

## Acceptance checks

1. The target preserves the three source conditions.
2. The negation in “has not already been refunded” remains explicit.
3. No new payment, legal, or policy claim is introduced.
4. The wording uses Simplified Chinese and natural Mainland China operational language.
5. A second reviewer can identify the same critical error from the visible source and target alone.

## 中文评测摘要

### 结论

**拒绝并修改。**

候选译文把“订单尚未退款”翻译成“订单已经退款”，丢失否定含义并反转业务条件。该错误可能让操作人员对已退款订单再次发起退款，因此定为严重度最高的准确性错误。

### 修订原则

1. 保留全部三个前置条件。
2. 明确保留“尚未退款”的否定含义。
3. 使用适合中国大陆业务操作场景的自然简体中文。
4. 不增加源文没有提供的支付、法律或政策信息。

## Reusable delivery format

An authorized evaluation project can reuse this structure:

1. Source, candidate target, and permitted reference material.
2. Evaluation taxonomy and severity definitions.
3. Evidence-linked error findings.
4. Corrected target.
5. Acceptance and second-review checks.

Customer source text, private benchmarks, terminology databases, model traces, and confidential guidelines must stay inside the customer-approved workspace and retention boundary.
