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
  <img alt="Average work output reduction" src="https://img.shields.io/badge/avg_output_reduction-86.8%25-18d48f">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-lightgrey">
</p>

`analpha` is a token-saving Codex skill that keeps assistant output minimal while still letting Codex do the actual work.

It is built for workflows where long explanations are noise: repeated checks, quick approvals, code review gates, operational triage, CI sanity checks, and “can I continue?” decisions.

By default, `analpha` answers with a simple approval or block signal:

```text
✅
```

or

```text
⛔
```

When something is blocked, unsafe, ambiguous, or requires user action, `analpha` can still speak up briefly.

The installed skill is still named `analphacodex` for compatibility, but the preferred command name is now `analpha`.

---

## What it is

Codex is useful, but it often talks too much.

For many tasks, you do not need a paragraph explaining that something passed. You need Codex to do the work, run the check, make the decision, and give you a fast signal.

`analpha` is for that.

| Situation | Output |
| --- | --- |
| Work completed | `✅` |
| Safe to continue | `✅` |
| Blocked | `⛔` |
| Unsafe / destructive / unclear | `⛔` + short reason |
| Explanation requested | Short explanation |
| Critical context missing | Short clarification |

Same work. Less output.

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

Normal Codex might respond with a long implementation summary, assumptions, reasoning, and test explanation.

With `analpha`, Codex still edits the files, runs the relevant checks if available, and then responds with:

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

## Benchmark Results

Benchmarks are measured with `tiktoken` using `o200k_base`.

These are controlled benchmark sets. They compare known normal outputs against known `analpha` outputs for the same prompts.

They are not automatic live Codex telemetry.

### Average work benchmark

This is the most representative benchmark for everyday usage.

Dataset:

```text
benchmarks/average_work_samples.jsonl
```

Scope:

```text
everyday coding, workplace, review, support, docs, and operational sanity-check prompts
```

Result:

```text
samples: 20
input/context tokens: 10880
normal output tokens: 816
analpha output tokens: 108
output tokens saved: 708
output reduction: 86.8%
normal total run tokens: 11696
analpha total run tokens: 10988
total run reduction with provided context: 6.1%
expected verdict matches: 20/20
```

Claim:

```text
For this controlled 20-question average-work sample set, analpha reduced assistant output tokens by 86.8% and total tokens by 6.1% when including provided context estimates.
```

### Real workload benchmark

Dataset:

```text
benchmarks/workload_effectiveness_samples.jsonl
```

Scope:

```text
frontend, infrastructure, CI, security, production operations, documentation, IAM, DNS, Kubernetes, Terraform, and logging
```

Result:

```text
samples: 20
input/context tokens: 618000
normal output tokens: 1160
analpha output tokens: 121
output tokens saved: 1039
output reduction: 89.6%
normal total run tokens: 619160
analpha total run tokens: 618121
total run reduction with provided context: 0.2%
expected verdict matches: 20/20
```

This benchmark includes approve and block cases:

```text
approve cases: 10
block cases: 10
critical/security-sensitive block cases: 8
expected verdict matches: 20/20
```

### Quick sanity checks

Dataset:

```text
benchmarks/usage_samples.jsonl
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

Dataset:

```text
benchmarks/large_usage_samples.jsonl
```

Result:

```text
samples: 4
input/context tokens: 310000
normal output tokens: 411
analpha output tokens: 29
output tokens saved: 382
output reduction: 92.9%
normal total run tokens: 310411
analpha total run tokens: 310029
total run reduction with provided context: 0.1%
```

---

## How to read the numbers

`analpha` is very good at reducing assistant output.

It does not magically remove huge input context.

If a run loads a massive codebase, diff, log dump, or tool context, total token savings will be smaller because most tokens are already spent before the assistant replies.

Honest claim:

```text
analpha reduces assistant output tokens significantly in the included benchmark samples.
```

Bad claim:

```text
analpha always saves 90% of all Codex tokens.
```

Real savings depend on how much context the task loads.

---

## Benchmark Your Own Workload

Install the tokenizer dependency once:

```bash
python -m pip install tiktoken
```

Run the provided benchmarks:

```bash
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/usage_samples.jsonl --details
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/average_work_samples.jsonl --details
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/workload_effectiveness_samples.jsonl --details
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

Use benchmarks for evidence.

Use stats only for rough local tracking.

---

## Safety Rule

When unsure, block.

`analpha` should not approve destructive, illegal, security-sensitive, high-cost, or ambiguous actions just to save tokens.

Smart mode may still explain briefly when the situation is critical.

Examples of things that should be blocked or require a short reason:

```text
⛔
No rollback evidence for destructive production migration.
```

```text
⛔
Do not expose internal admin dashboards publicly.
```

```text
⛔
Missing backup confirmation before deleting shared storage.
```

```text
⛔
Do not paste API tokens into GitHub issues.
```

---

## When not to use it

Do not use `analpha` when you actually need reasoning, teaching, planning, or detailed debugging output.

Good fit:

```text
- approval checks
- repeated review gates
- quick “safe or not?” decisions
- CI sanity decisions
- simple done/blocked reporting
- high-volume Codex workflows
```

Bad fit:

```text
- learning a new concept
- architecture explanations
- debugging without enough context
- writing documentation from scratch
- tasks where you need a detailed audit trail
```

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

---

## License

MIT
