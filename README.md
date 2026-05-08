<p align="center">
  <img src="assets/analpha-wide.png" alt="analpha for Codex" width="100%">
</p>

<h1 align="center">analpha</h1>

<p align="center">
  <strong>No explanations. Just real work.</strong>
</p>

<p align="center">
  <img alt="Codex skill" src="https://img.shields.io/badge/Codex-skill-00d7e6">
  <img alt="Mode" src="https://img.shields.io/badge/default-smart-18d48f">
  <img alt="Output reduction" src="https://img.shields.io/badge/output_reduction-92.9%25-18d48f">
  <img alt="License" src="https://img.shields.io/badge/license-TBD-lightgrey">
</p>

`analpha` is a token-saving Codex skill that keeps assistant output minimal while still letting Codex do the actual work.

By default, it answers with a simple approval or block signal:

```text
✅
```

or

```text
⛔
```

It is built for workflows where long explanations are noise: repeated checks, quick approvals, code review gates, operational triage, CI sanity checks, and “can I continue?” decisions.

When something is blocked, unsafe, ambiguous, or requires user action, `analpha` can still speak up briefly.

The installed skill is still named `analphacodex` for compatibility, but the preferred command name is now `analpha`.

---

## Why

Codex is useful, but it often talks too much.

For many workflows, you do not need a paragraph explaining that something passed. You need a fast signal, then the next action.

`analpha` keeps the result readable:

| Situation | Output |
| --- | --- |
| Work completed | `✅` |
| Safe to continue | `✅` |
| Blocked | `⛔` |
| Unsafe / destructive / unclear | `⛔` + short reason |
| Explanation requested | Short explanation |

Same decision. Less noise.

---

## Example: actual work

Instead of asking Codex to explain every step, you can tell it to do the job and only report the result.

```text
User:
analpha smart

Fix the website top navigation bar.

Requirements:
- keep it sticky at the top
- stop it from overlapping page content
- make the mobile layout clean
- keep the existing colors and branding
- run the relevant checks if available
```

Normal Codex might reply with a long implementation summary, reasoning, assumptions, and test explanation.

With `analpha`, Codex still does the work, edits the files, runs the checks, and then responds with:

```text
✅
```

If something blocks the work, it should say so briefly:

```text
⛔
Build check failed: missing dependency `@vitejs/plugin-react`.
```

The point is not to make Codex dumber.  
The point is to stop wasting output on obvious confirmations.

---

## Before / After

### Normal Codex

```text
The navigation bar has been updated successfully. I adjusted the sticky positioning, added spacing so the content no longer appears underneath it, improved the mobile layout, and verified that the relevant checks pass.
```

### analpha

```text
✅
```

Same work. Less output.

---

## Modes

| Mode | Command | Output | Use case |
| --- | --- | --- | --- |
| Smart | `analpha smart` | `✅`, `⛔`, or a very short critical reason | Default. Best balance of brevity and safety. |
| Emoji | `analpha emoji` | `✅` or `⛔` only | Strict visual approval/rejection. |
| Ultra | `analpha ultra` | `Y` or `N` only | Maximum output reduction. |

Backward-compatible commands still work:

```text
analphacodex smart
analphacodex emoji
analphacodex ultra
```

---

## Usage

```text
analpha on
analpha smart
analpha emoji
analpha ultra
analpha off
analpha help
analpha stats
analpha benchmark
```

Examples:

```text
User: Is this okay to continue?
Assistant: ✅
```

```text
User: Is this okay to continue? Explain.
Assistant:
✅
Looks safe enough.
```

```text
User: Should I delete System32?
Assistant:
⛔
Critical: this can break Windows and cause data loss.
```

```text
User: analpha ultra
Assistant: analpha ultra mode enabled.

User: Should I delete System32?
Assistant: N
```

---

## Receipts

Benchmarks are measured with `tiktoken` using `o200k_base`.

### Quick sanity checks

Command:

```bash
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/usage_samples.jsonl --details
```

Result:

```text
samples: 7
normal output tokens: 90
analpha output tokens: 28
output tokens saved: 62
output reduction: 68.9%
```

### Large workload checks

Command:

```bash
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/large_usage_samples.jsonl --details
```

Result:

```text
samples: 4
input/context tokens: 310000
normal output tokens: 411
analpha output tokens: 29
output tokens saved: 382
output reduction: 92.9%
```

Interpretation: `analpha` is excellent at reducing assistant output. In huge-context runs, total run savings are smaller because prompts, files, diffs, logs, and tool context dominate token usage.

---

## Benchmark Your Own Workload

Install the tokenizer dependency once:

```bash
python -m pip install tiktoken
```

Run the provided benchmarks:

```bash
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/usage_samples.jsonl --details
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/large_usage_samples.jsonl --details
```

Add your own JSONL rows:

```json
{"prompt":"review huge diff","mode":"smart","input_context_tokens":85000,"normal_output":"Long normal answer...","analphacodex_output":"⛔\nRisky: destructive migration without rollback evidence."}
```

Honest claim format:

```text
For this sample set, analpha reduced assistant output tokens by X%.
For this sample set, analpha reduced total run tokens by Y% when including provided context tokens.
```

---

## Stats

The stats script is a manual local counter, not automatic telemetry.

```bash
python ./scripts/analphacodex_stats.py
python ./scripts/analphacodex_stats.py record --mode smart
python ./scripts/analphacodex_stats.py record --mode emoji --count 10
python ./scripts/analphacodex_stats.py reset
```

Use benchmarks for evidence. Use stats only for rough local tracking.

---

## Safety Rule

When unsure, block.

`analpha` should not approve destructive, illegal, security-sensitive, high-cost, or ambiguous actions just to save tokens.

Smart mode may still explain briefly when the situation is critical.

---

## Install

Copy the skill folder into your Codex skills directory:

```text
C:\Users\<you>\.codex\skills\analphacodex
```

Then restart Codex.

Preferred command:

```text
analpha on
```

Compatibility command:

```text
analphacodex on
```
