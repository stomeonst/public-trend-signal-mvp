# Bilingual Python Code Review Sample

Review date: 2026-07-27

Scope: one small fictional Python function. No customer code, private repository, credentials, or production data is included.

Candidate fixture:
[`examples/python_review_candidate.py`](../examples/python_review_candidate.py)

Reference correction:
[`examples/python_review_reference.py`](../examples/python_review_reference.py)

## English review

### Verdict

The candidate works for a narrow happy path, but it is not reliable enough for repeated evaluation tasks.

### Findings

1. **High: a rejected title can suppress a later eligible record.**  
   The code adds every title to `seen`, including records below `minimum_score`. If a low-scoring record appears first and the same title later meets the threshold, the eligible record is incorrectly omitted.

2. **Medium: normalization is incomplete.**  
   `strip()` removes only leading and trailing whitespace. Titles such as `"AI   Workflow"` and `"ai workflow"` remain separate even when the intended identity is case-insensitive and whitespace-normalized.

3. **Medium: malformed records fail with unclear built-in exceptions.**  
   Missing keys, non-string titles, and non-numeric scores raise different incidental exceptions. A caller cannot identify the failing record consistently.

4. **Low: the input and output contract is implicit.**  
   Type hints and an explicit validation policy make the function easier to review and reuse.

### Minimal counterexample

```python
records = [
    {"title": "Same signal", "score": 1},
    {"title": "Same signal", "score": 10},
]

unique_recent_titles(records, minimum_score=5)
```

Expected: `["Same signal"]`

Candidate result: `[]`

### Complexity

For `n` records and total title length `m`, the reference correction runs in `O(n + m)` time and uses `O(k + m)` additional space for `k` unique accepted identities and their normalized text.

## 中文评审

### 结论

候选实现可以处理范围很窄的常见输入，但无法稳定覆盖重复评审任务。

### 发现

1. **高优先级：未达阈值的标题会错误拦截后续合格记录。**  
   代码把所有标题加入`seen`，其中也包含低于`minimum_score`的记录。如果低分记录先出现，而同名高分记录随后出现，后者会被错误遗漏。

2. **中优先级：标准化不完整。**  
   `strip()`只删除首尾空白。`"AI   Workflow"`与`"ai workflow"`仍会被视为不同标题，即使业务身份规则要求忽略大小写并合并空白。

3. **中优先级：异常记录产生的错误不清晰。**  
   缺少字段、标题类型错误和分数类型错误会触发不同的偶然异常，调用方无法稳定定位失败记录。

4. **低优先级：输入输出契约缺少显式说明。**  
   类型标注和明确的验证策略可以提高可审查性与可复用性。

### 最小反例

```python
records = [
    {"title": "Same signal", "score": 1},
    {"title": "Same signal", "score": 10},
]

unique_recent_titles(records, minimum_score=5)
```

预期结果：`["Same signal"]`

候选结果：`[]`

### 复杂度

设记录数为`n`，标题总长度为`m`。参考修复的时间复杂度为`O(n + m)`，额外空间复杂度为`O(k + m)`，其中`k`为合格的唯一标题身份数量。
