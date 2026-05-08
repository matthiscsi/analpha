# analpha average work effectiveness report

This report measures `analpha` on average work conversations, not huge codebase or log-review runs.

Dataset:

- File: `benchmarks/average_work_samples.jsonl`
- Samples: 20
- Measurement: exact `tiktoken` count with `o200k_base`
- Scope: everyday coding, workplace, review, support, docs, and operational sanity-check prompts

Important: this is a controlled benchmark set. It compares known normal outputs against known `analpha` outputs for the same questions. It does not claim automatic live Codex telemetry.

## Why This Matters

The previous huge-context benchmark showed strong output reduction but weak total-run reduction because the input context was enormous:

```text
huge workload total-run reduction: 0.2%
```

That is not the main target environment for `analpha`.

The main target is average work where the interaction is mostly conversational and the user needs a verdict, not a paragraph.

## Exact Token Results

Generated with:

```bash
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/average_work_samples.jsonl --details
```

```text
analpha benchmark:
- measurement: exact tiktoken encoding o200k_base
- samples: 20
- input/context tokens: 10880
- normal output tokens: 816
- analpha output tokens: 108
- output tokens saved for sample set: 708
- output reduction for sample set: 86.8%
- normal total run tokens: 11696
- analpha total run tokens: 10988
- total run reduction with provided context: 6.1%

details:
1. smart: context=420, normal_output=47, analpha_output=1, output_saved=46
2. smart: context=850, normal_output=47, analpha_output=1, output_saved=46
3. smart: context=520, normal_output=68, analpha_output=12, output_saved=56
4. emoji: context=250, normal_output=27, analpha_output=1, output_saved=26
5. ultra: context=300, normal_output=23, analpha_output=1, output_saved=22
6. smart: context=700, normal_output=50, analpha_output=15, output_saved=35
7. smart: context=380, normal_output=63, analpha_output=16, output_saved=47
8. smart: context=900, normal_output=53, analpha_output=1, output_saved=52
9. emoji: context=450, normal_output=26, analpha_output=3, output_saved=23
10. ultra: context=180, normal_output=26, analpha_output=1, output_saved=25
11. smart: context=620, normal_output=53, analpha_output=14, output_saved=39
12. smart: context=950, normal_output=52, analpha_output=1, output_saved=51
13. smart: context=220, normal_output=37, analpha_output=7, output_saved=30
14. emoji: context=650, normal_output=25, analpha_output=1, output_saved=24
15. ultra: context=260, normal_output=17, analpha_output=1, output_saved=16
16. smart: context=350, normal_output=42, analpha_output=13, output_saved=29
17. smart: context=1100, normal_output=46, analpha_output=1, output_saved=45
18. smart: context=500, normal_output=44, analpha_output=14, output_saved=30
19. emoji: context=520, normal_output=26, analpha_output=3, output_saved=23
20. smart: context=760, normal_output=44, analpha_output=1, output_saved=43
```

## Dataset Shape

The set includes:

- small coding checks
- commit/message review
- CSS and docs approvals
- safe/unsafe shell command sanity checks
- dependency update approval
- incident/ticket communication checks
- security-sensitive workplace decisions
- production change checks

Safety balance:

- Approve cases: 10
- Block cases: 10
- Expected verdict matches: 20/20

## Conclusion

For average work conversations, `analpha` performs much better than the huge-context total-run case because input context is smaller and assistant reply size is a larger part of the interaction.

Use this claim:

```text
For this controlled 20-question average-work sample set, analpha reduced assistant output tokens by 86.8% and total tokens by 6.1% when including provided context estimates.
```

Do not use this claim:

```text
analpha always saves Y% of all Codex tokens.
```

That would be too broad. Real savings depend on how much context the task loads.

