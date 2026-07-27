# Simplified Chinese AI Output Evaluation Sample

## Scope and evidence boundary

This is a fictional public demonstration prepared to show a reproducible evaluation method. It contains no customer prompt, model trace, private benchmark, personal data, confidential guideline, or production result.

The sample evaluates one short Simplified Chinese answer for factual support, instruction following, language quality, localization, and risk handling. Scores are tied to visible evidence so another reviewer can reproduce the decision.

## Fictional task

User request:

> 请用不超过80个汉字，向第一次使用自动化工具的小店经营者解释什么是人工复核，并给出一个订单退款场景。不要承诺系统永远不会出错。

Candidate answer:

> 人工复核是让工作人员检查系统自动作出的决定。例如，系统发现订单可能需要退款时，店员会核对付款记录和客户说明，再决定是否退款。这样可以保证所有结果绝对正确。

Reference facts available to the reviewer:

1. Automated decisions can be reviewed by a person before a consequential action.
2. Refund review may use payment records, order status, and customer supplied context.
3. Human review reduces risk but does not guarantee perfect outcomes.

## Evaluation rubric

| Dimension | Weight | Pass condition |
| --- | ---: | --- |
| Instruction following | 25 | Uses no more than 80 Chinese characters, explains human review, gives a refund example, and avoids an absolute guarantee |
| Factual support | 25 | Every material claim is supported by the provided facts |
| Simplified Chinese quality | 20 | Natural Mainland China wording, correct grammar and punctuation, no Traditional Chinese leakage |
| Usefulness and clarity | 20 | A first time automation user can understand who reviews what and when |
| Risk handling | 10 | Preserves uncertainty and avoids presenting review as infallible |

## Review result

### Overall decision

**Needs revision, 62 out of 100.**

The answer explains the concept clearly and includes a relevant refund example. The final sentence makes an unsupported absolute guarantee and directly violates the instruction.

### Dimension scores

| Dimension | Score | Evidence |
| --- | ---: | --- |
| Instruction following | 10 / 25 | The answer covers human review and a refund scenario, but “保证所有结果绝对正确” violates the explicit constraint |
| Factual support | 17 / 25 | The process description is supported; the perfect outcome claim is unsupported |
| Simplified Chinese quality | 20 / 20 | Wording, grammar, punctuation, and register are natural for a general Mainland China audience |
| Usefulness and clarity | 15 / 20 | The reviewer, evidence, and decision are understandable; the timing of review could be more explicit |
| Risk handling | 0 / 10 | The final sentence removes uncertainty and overstates reliability |

### Severity tagged findings

1. **High, unsupported guarantee.** “保证所有结果绝对正确” contradicts the task and the supplied facts. It may create false confidence around a consequential refund decision.
2. **Medium, review timing is implicit.** The answer would be clearer if it stated that the shop assistant checks the evidence before the refund is issued.
3. **Low, evidence list can be slightly more concrete.** Adding order status would align the example more closely with the supplied facts.

## Reference revision

> 人工复核是由工作人员在系统执行重要操作前检查依据。例如，退款前，店员会核对付款记录、订单状态和客户说明，再决定是否退款，以降低误判风险。

Character count for the reference revision: 68 characters including punctuation.

## 中文评审摘要

### 结论

**需要修改，62分。**

候选回答完成了概念解释和退款举例，语言自然清晰。结尾的“保证所有结果绝对正确”属于无依据的绝对承诺，违反了用户的明确要求，也会放大退款决策中的信任风险。

### 修改理由

1. 删除绝对正确的承诺。
2. 明确人工复核发生在退款执行之前。
3. 补充订单状态这一项可核验依据。
4. 使用“降低误判风险”表达合理收益，同时保留不确定性。

## Reviewer consistency checks

Before accepting a score, a second reviewer should confirm:

1. The character count method is documented and applied consistently.
2. Every factual criticism points to the supplied reference facts or the user instruction.
3. Language preference is separated from correctness and safety.
4. An absolute claim receives the same severity regardless of whether the answer is otherwise fluent.
5. The reference revision fixes the cited issues without adding unsupported facts.

## Reusable delivery format

A real authorized engagement can use the same artifact shape:

1. Input task and permitted reference material.
2. Weighted rubric and explicit pass conditions.
3. Dimension scores with evidence.
4. Severity tagged findings.
5. Reference revision.
6. Second reviewer consistency checks.

Customer prompts, private benchmark data, model traces, and confidential guidelines must remain in the customer approved workspace and retention boundary.
