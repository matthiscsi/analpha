# analpha benchmark receipts

Measured with:

```bash
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/usage_samples.jsonl --details
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/large_usage_samples.jsonl --details
```

Tokenizer:

```text
tiktoken o200k_base
```

## Quick sanity checks

```text
analpha benchmark:
- measurement: exact tiktoken encoding o200k_base
- samples: 7
- input/context tokens: 0
- normal output tokens: 90
- analpha output tokens: 28
- output tokens saved for sample set: 62
- output reduction for sample set: 68.9%

details:
1. smart: context=0, normal_output=9, analpha_output=1, output_saved=8
2. smart: context=0, normal_output=21, analpha_output=6, output_saved=15
3. smart: context=0, normal_output=20, analpha_output=15, output_saved=5
4. emoji: context=0, normal_output=11, analpha_output=1, output_saved=10
5. emoji: context=0, normal_output=12, analpha_output=3, output_saved=9
6. ultra: context=0, normal_output=9, analpha_output=1, output_saved=8
7. ultra: context=0, normal_output=8, analpha_output=1, output_saved=7
```

## Large workload checks

```text
analpha benchmark:
- measurement: exact tiktoken encoding o200k_base
- samples: 4
- input/context tokens: 310000
- normal output tokens: 411
- analpha output tokens: 29
- output tokens saved for sample set: 382
- output reduction for sample set: 92.9%
- normal total run tokens: 310411
- analpha total run tokens: 310029
- total run reduction with provided context: 0.1%

details:
1. smart: context=85000, normal_output=134, analpha_output=13, output_saved=121
2. smart: context=120000, normal_output=123, analpha_output=12, output_saved=111
3. emoji: context=65000, normal_output=99, analpha_output=3, output_saved=96
4. ultra: context=40000, normal_output=55, analpha_output=1, output_saved=54
```

## Interpretation

These results support this claim:

```text
For the included benchmark samples, analpha reduced assistant output tokens by 68.9% on quick checks and 92.9% on large workload checks.
```

They do not prove exact live savings unless real production outputs and a matching baseline are captured.
