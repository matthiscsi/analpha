# analpha effectiveness report

This report measures whether `analpha` reduces assistant output in realistic workload interactions.

Dataset:

- File: `benchmarks/workload_effectiveness_samples.jsonl`
- Samples: 20
- Measurement: exact `tiktoken` count with `o200k_base`
- Scope: assistant output reduction and total-run impact when provided context-token estimates are included

Important: this is a controlled benchmark set. It measures known normal outputs against known `analpha` outputs for the same questions. It does not claim automatic live Codex telemetry.

## Workload Prompts Tested

The set includes real workplace-style prompts across frontend, infrastructure, CI, security, production operations, documentation, IAM, DNS, Kubernetes, Terraform, and logging.

Example prompt:

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

Expected `analpha` result:

```text
âœ…
```

## Exact Token Results

Generated with:

```bash
python ./scripts/analphacodex_benchmark.py --input ./benchmarks/workload_effectiveness_samples.jsonl --details
```

```text
analpha benchmark:
- measurement: exact tiktoken encoding o200k_base
- samples: 20
- input/context tokens: 618000
- normal output tokens: 1160
- analpha output tokens: 121
- output tokens saved for sample set: 1039
- output reduction for sample set: 89.6%
- normal total run tokens: 619160
- analpha total run tokens: 618121
- total run reduction with provided context: 0.2%

details:
1. smart: context=42000, normal_output=99, analpha_output=1, output_saved=98
2. smart: context=98000, normal_output=100, analpha_output=13, output_saved=87
3. emoji: context=12000, normal_output=58, analpha_output=3, output_saved=55
4. ultra: context=9000, normal_output=38, analpha_output=1, output_saved=37
5. smart: context=135000, normal_output=91, analpha_output=13, output_saved=78
6. smart: context=28000, normal_output=82, analpha_output=18, output_saved=64
7. emoji: context=15000, normal_output=50, analpha_output=3, output_saved=47
8. ultra: context=11000, normal_output=29, analpha_output=1, output_saved=28
9. smart: context=55000, normal_output=59, analpha_output=1, output_saved=58
10. smart: context=6000, normal_output=65, analpha_output=12, output_saved=53
11. emoji: context=24000, normal_output=42, analpha_output=1, output_saved=41
12. smart: context=33000, normal_output=65, analpha_output=15, output_saved=50
13. ultra: context=8000, normal_output=25, analpha_output=1, output_saved=24
14. smart: context=5000, normal_output=50, analpha_output=8, output_saved=42
15. smart: context=31000, normal_output=63, analpha_output=1, output_saved=62
16. emoji: context=7000, normal_output=43, analpha_output=3, output_saved=40
17. smart: context=46000, normal_output=63, analpha_output=9, output_saved=54
18. ultra: context=13000, normal_output=31, analpha_output=1, output_saved=30
19. smart: context=18000, normal_output=46, analpha_output=1, output_saved=45
20. smart: context=22000, normal_output=61, analpha_output=15, output_saved=46
```

## Safety Results

The test set includes both approve and block cases.

- Approve cases: 10
- Block cases: 10
- Critical/security-sensitive block cases: 8
- Expected verdict matches: 20/20

Block scenarios include:

- destructive production database migration without rollback proof
- public exposure of an internal admin dashboard
- deletion on shared storage without backup confirmation
- public RDP exposure
- pasting API tokens into GitHub issues
- unsafe production Kubernetes restart
- disabling MFA temporarily
- logging Authorization/Cookie headers into shared observability

## What The Numbers Mean

The useful claim is:

```text
For this controlled workload sample set, analpha reduced assistant output tokens by the measured percentage below.
```

The careful caveat is:

```text
Total run reduction is much smaller when huge file, diff, log, and tool context is included.
```

That distinction matters. `analpha` is built to stop long replies after work is done. It does not make large input context disappear.

## Conclusion

`analpha` is effective for workload environments where the assistant is already doing real work and the user only needs the final approval, rejection, or safety verdict.

Motto:

```text
No explanations. Just real work.
```

