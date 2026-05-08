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

`analpha` is a token-saving Codex skill that keeps Codex quiet after the work is done.

Instead of long confirmations, summaries, and obvious explanations, it returns a simple signal:

```text
✅
```

or:

```text
⛔
```

Codex still does the work.  
`analpha` just reduces the noise.

It is useful for repeated checks, quick approvals, code review gates, CI sanity checks, operational triage, and “can I continue?” decisions.

When something is blocked, unsafe, ambiguous, or needs user action, `analpha` can still speak briefly.

The installed skill is still named `analphacodex` for compatibility, but the preferred command name is now `analpha`.

---

## What it does

| Situation | Output |
| --- | --- |
| Work completed | `✅` |
| Safe to continue | `✅` |
| Blocked | `⛔` |
| Unsafe / destructive / unclear | `⛔` + short reason |
| Explanation requested | Short explanation |
| Critical context missing | Short clarification |

The goal is simple:

```text
same work, less output
```

---

## Example: actual work

Use it when you want Codex to fix something, not explain the obvious.

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

Normal Codex might reply with a long summary of what it changed.

With `analpha`, Codex still edits the files and runs the checks, but the final response becomes:

```text
✅
```

If something blocks the work:

```text
⛔
Build check failed: missing dependency `@vitejs/plugin-react`.
```

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

Same result. Fewer tokens.

---

## Modes

| Mode | Command | Output | Use case |
| --- | --- | --- | --- |
| Smart | `analpha smart` | `✅`, `⛔`, or short critical reason | Default mode. Brief, but still safe. |
| Emoji | `analpha emoji` | `✅` or `⛔` only | Strict approval/block signal. |
| Ultra | `analpha ultra` | `Y` or `N` only | Maximum output reduction. |

Backward-compatible commands:

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

## Benchmarks

Measured with `tiktoken` using `o200k_base`.

These are controlled local benchmark sets, not live Codex telemetry.

| Benchmark | Samples | Output reduction | Total run reduction |
| --- | ---: | ---: | ---: |
| Average work | 20 | 86.8% | 6.1% |
| Real workload | 20 | 89.6% | 0.2% |
| Quick sanity checks | 7 | 68.9% | N/A |
| Large workload checks | 4 | 92.9% | 0.1% |

Important: `analpha` reduces assistant output. It does not remove large input context.

If a run loads huge files, diffs, logs, or tool context, total token savings will be smaller because most tokens are already spent before the final reply.

Good claim:

```text
analpha reduces assistant output tokens significantly in the included benchmark samples.
```

Bad claim:

```text
analpha always saves 90% of all Codex tokens.
```

---

## Run benchmarks

Install dependency:

```bash
python -m pip install tiktoken
```

Run:

```bash
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/usage_samples.jsonl --details
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/average_work_samples.jsonl --details
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/workload_effectiveness_samples.jsonl --details
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/large_usage_samples.jsonl --details
```

---

## Stats

The stats script is a manual local counter, not telemetry.

```bash
python ./scripts/analphacodex_stats.py
python ./scripts/analphacodex_stats.py record --mode smart
python ./scripts/analphacodex_stats.py record --mode emoji --count 10
python ./scripts/analphacodex_stats.py reset
```

---

## Safety Rule

When unsure, block.

`analpha` should not approve destructive, illegal, security-sensitive, high-cost, or ambiguous actions just to save tokens.

Examples:

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

## When to use it

Good fit:

```text
- approval checks
- repeated review gates
- quick safe/not-safe decisions
- CI sanity decisions
- simple done/blocked reporting
- high-volume Codex workflows
```

Bad fit:

```text
- learning
- architecture explanations
- detailed debugging
- writing documentation from scratch
- tasks where you need a full audit trail
```

---

## Install

Copy the skill folder into your Codex skills directory:

```text
C:\Users\<you>\.codex\skills\analphacodex
```

Restart Codex.

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
