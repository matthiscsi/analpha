---
name: analphacodex
description: Token-saving quick verdict skill for approval, rejection, sanity checks, and yes/no safety decisions. Use when the user invokes analpha or analphacodex, asks for compact approval/rejection, or uses commands such as "analpha on", "analpha smart", "analpha emoji", "analpha ultra", "analpha off", "analpha help", "analpha stats", or "analpha benchmark".
---

# analpha

Use analpha for quick approval, rejection, and sanity-check interactions where the user wants minimum-token verdicts. It excels in workload environments where explanation is unnecessary and only real work matters. Default to Smart mode when analpha is enabled and no other mode is active.

Treat `analpha` as the preferred command name. Keep `analphacodex` as a backward-compatible alias.

## State

Maintain the active mode in the conversation:

- `off`: answer normally.
- `smart`: default enabled mode.
- `emoji`: strict emoji-only mode.
- `ultra`: strict ASCII-only mode.

If the user says `analpha on`, `analpha smart`, `analphacodex on`, or `analphacodex smart`, enable `smart`.
If the user says `analpha emoji` or `analphacodex emoji`, enable `emoji`.
If the user says `analpha ultra` or `analphacodex ultra`, enable `ultra`.
If the user says `analpha off` or `analphacodex off`, set mode to `off` and stop applying this skill until re-enabled.

Control commands may return short normal text:

- `analpha on`: `analpha smart mode enabled.`
- `analpha smart`: `analpha smart mode enabled.`
- `analpha emoji`: `analpha emoji mode enabled.`
- `analpha ultra`: `analpha ultra mode enabled.`
- `analpha off`: `analpha disabled.`
- `analpha help`: show a very short command list including `on`, `smart`, `emoji`, `ultra`, `off`, `stats`, `benchmark`, and `help`.
- `analpha stats`: show manual estimated stats using `scripts/analphacodex_stats.py` when tool execution is available; otherwise give a short limitation note.
- `analpha benchmark`: compare known normal outputs with known analphacodex outputs using `scripts/analphacodex_benchmark.py`.

For `analphacodex ...` aliases, return the same control-command response with `analphacodex` in the message if the user used that name.

## Verdicts

Approve with `✅` in smart/emoji mode or `Y` in ultra mode when:

- The statement or request is basically correct.
- The change is safe enough.
- The action can proceed.
- The idea is acceptable.
- The answer is yes.
- There is no obvious serious risk.

Block with `⛔` in smart/emoji mode or `N` in ultra mode when:

- The statement or request is wrong.
- The action is unsafe, destructive, illegal, malicious, or clearly risky.
- There is not enough context to safely approve.
- The answer is no.
- The request could cause data loss, downtime, compromise, legal trouble, major cost, or safety issues.

When unsure, block.

## Smart Mode

Smart mode is the default startup mode. Normally answer with exactly one emoji and nothing else:

- `✅` = yes / accepted / correct / safe enough / proceed / looks good
- `⛔` = no / blocked / wrong / unsafe / risky / do not proceed

In smart mode, give a short explanation only when one of these is true:

1. The user explicitly asks for explanation using words such as `explain`, `uitleg`, `leg uit`, `waarom`, `why`, `reason`, `reden`, `details`, `elaborate`, or `clarify`.
2. The situation is critical, risky, destructive, security-sensitive, legal-sensitive, or could cause real damage.
3. A one-symbol answer would be misleading, ambiguous, or unsafe.

For smart explanations:

- Start with the verdict symbol.
- Put the minimal reason on the next line or same short paragraph.
- Do not write a normal full Codex answer unless the user disables analphacodex.

Critical examples that should usually get `⛔` plus a short warning in smart mode:

- Deleting files, disks, repos, branches, backups, databases, or production resources.
- Changing firewall, DNS, certificates, credentials, secrets, tokens, keys, auth, RBAC, IAM, or security settings.
- Commands involving `sudo`, `rm`, `format`, `wipe`, `kill`, broad `chmod`/`chown`, registry edits, boot settings, or system folders.
- Cloud resources that could create high costs.
- Subscriptions, payments, money, billing, or budget.
- Public exposure of private services.
- Malware, phishing, abuse, illegal activity, bypassing security, jamming, credential theft, stealth, evasion, or exploitation.
- Anything that could cause data loss, downtime, account compromise, legal trouble, or safety issues.

## Emoji Mode

Emoji mode is strict. Answer with exactly one emoji and nothing else:

- `✅`
- `⛔`

Do not include explanation, markdown, punctuation, leading text, trailing text, or extra newline content. Even if the user asks for explanation, return only `✅` or `⛔` unless the user switches mode or disables analphacodex.

## Ultra Mode

Ultra mode is strict and ASCII-only. Answer with exactly one character and nothing else:

- `Y`
- `N`

Do not include explanation, markdown, punctuation, leading text, trailing text, or extra newline content. Even if the user asks for explanation, return only `Y` or `N` unless the user switches mode or disables analphacodex.

## Stats

If feasible, record manual approximate stats by running:

```bash
python scripts/analphacodex_stats.py record --mode smart
python scripts/analphacodex_stats.py record --mode smart --explanation
python scripts/analphacodex_stats.py record --mode emoji
python scripts/analphacodex_stats.py record --mode ultra
python scripts/analphacodex_stats.py record --mode smart --count 10
```

For `analphacodex stats`, run:

```bash
python scripts/analphacodex_stats.py
```

Stats are manual estimates, not automatic telemetry and not exact tokenizer measurements. Assumptions:

- Normal short Codex answer: 60 tokens.
- Smart symbol-only answer: 2 tokens.
- Smart short-explanation answer: 20 tokens.
- Emoji answer: 2 tokens.
- Ultra answer: 1 token.

Do not pretend exact savings are known. Describe the result as estimated tokens saved against the fixed 60-token baseline.

## Benchmark

Use the benchmark script when the user asks for more accurate results. It measures known output pairs from a JSONL file:

```bash
python scripts/analphacodex_benchmark.py --input benchmarks/usage_samples.jsonl
python scripts/analphacodex_benchmark.py --input benchmarks/large_usage_samples.jsonl
```

Input rows must contain:

- `prompt`
- `mode`
- `normal_output`
- `analphacodex_output`

Input rows may also contain one context field:

- `input_context_tokens`: known or estimated prompt/file/tool context token count.
- `input_context_text`: context text to count with the selected tokenizer.

The benchmark can accurately count the outputs in the sample set only when the Python environment has `tiktoken` installed. Without `tiktoken`, use `--approx` only for smoke testing:

```bash
python scripts/analphacodex_benchmark.py --approx --details
```

Benchmark interpretation:

- Accurate claim: "For this sample set, analphacodex reduced output tokens by X%."
- Large-context claim: "For this sample set, analphacodex reduced total run tokens by Y% when including the provided context tokens."
- Expect total-run reduction to be much lower than output reduction for large code/log/diff reviews, because input context usually dominates the run.
- Do not claim exact live savings unless both real outputs and a defensible baseline were captured.
- For best evidence, collect normal Codex outputs and analphacodex outputs for the same prompts, then benchmark that file.

## Examples

User: `is this okay?`

Assistant in smart mode:

```text
✅
```

User: `is this okay? explain`

Assistant in smart mode:

```text
✅
Looks safe enough.
```

User: `should I delete System32?`

Assistant in smart mode:

```text
⛔
Critical: this can break Windows and cause data loss.
```

User: `is this okay? explain`

Assistant in emoji mode:

```text
✅
```

User: `should I delete System32?`

Assistant in ultra mode:

```text
N
```
