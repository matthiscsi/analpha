# analphacodex examples

## Smart mode

```text
User: analphacodex smart
Assistant: analphacodex smart mode enabled.
```

```text
User: is this okay?
Assistant: ✅
```

```text
User: is this okay? explain
Assistant:
✅
Looks safe enough.
```

```text
User: should I delete System32?
Assistant:
⛔
Critical: this can break Windows and cause data loss.
```

## Emoji mode

```text
User: analphacodex emoji
Assistant: analphacodex emoji mode enabled.
```

```text
User: is this okay? explain
Assistant: ✅
```

```text
User: should I delete System32?
Assistant: ⛔
```

## Ultra mode

```text
User: analphacodex ultra
Assistant: analphacodex ultra mode enabled.
```

```text
User: is this okay?
Assistant: Y
```

```text
User: should I delete System32?
Assistant: N
```

## Stats

```text
User: analphacodex stats
Assistant:
analphacodex manual estimated stats:
- recorded replies: 1
- smart: 1
- emoji: 0
- ultra: 0
- smart explanations: 0
- assumed baseline tokens: 60
- estimated analphacodex tokens: 2
- estimated tokens saved vs baseline: 58
- estimated reduction vs baseline: 96.7%
Note: manual counter only; not automatic telemetry or exact tokenizer measurement.
```

## Benchmark

```text
Command:
python scripts/analphacodex_benchmark.py --input benchmarks/usage_samples.jsonl --details

Output shape:
analphacodex benchmark:
- measurement: exact tiktoken encoding o200k_base
- samples: 7
- normal output tokens: <count>
- analphacodex output tokens: <count>
- tokens saved for sample set: <count>
- reduction for sample set: <percent>
```

Actual numbers depend on the benchmark samples and tokenizer encoding.

Large-context benchmark:

```text
Command:
python scripts/analphacodex_benchmark.py --input benchmarks/large_usage_samples.jsonl --details

Output shape:
analphacodex benchmark:
- measurement: exact tiktoken encoding o200k_base
- samples: <count>
- input/context tokens: <count>
- normal output tokens: <count>
- analphacodex output tokens: <count>
- output tokens saved for sample set: <count>
- output reduction for sample set: <percent>
- normal total run tokens: <count>
- analphacodex total run tokens: <count>
- total run reduction with provided context: <percent>
```
