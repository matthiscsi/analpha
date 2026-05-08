#!/usr/bin/env python3
"""Benchmark analpha output tokens against normal output tokens."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


DEFAULT_INPUT = Path(__file__).resolve().parents[1] / "benchmarks" / "usage_samples.jsonl"


@dataclass(frozen=True)
class Sample:
    prompt: str
    mode: str
    normal_output: str
    analphacodex_output: str
    input_context_tokens: int | None = None
    input_context_text: str | None = None


@dataclass(frozen=True)
class CountedSample:
    sample: Sample
    normal_tokens: int
    analphacodex_tokens: int
    context_tokens: int

    @property
    def saved_tokens(self) -> int:
        return self.normal_tokens - self.analphacodex_tokens


def load_samples(path: Path) -> list[Sample]:
    samples: list[Sample] = []

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSON: {exc}") from exc

            samples.append(parse_sample(record, path, line_number))

    if not samples:
        raise SystemExit(f"{path}: no benchmark samples found")

    return samples


def parse_sample(record: dict[str, Any], path: Path, line_number: int) -> Sample:
    required = ["prompt", "mode", "normal_output", "analphacodex_output"]
    missing = [key for key in required if key not in record]
    if missing:
        raise SystemExit(f"{path}:{line_number}: missing fields: {', '.join(missing)}")

    values = {key: record[key] for key in required}
    for key, value in values.items():
        if not isinstance(value, str) or not value.strip():
            raise SystemExit(f"{path}:{line_number}: {key} must be a non-empty string")

    if values["mode"] not in {"smart", "emoji", "ultra"}:
        raise SystemExit(f"{path}:{line_number}: mode must be smart, emoji, or ultra")

    input_context_tokens = record.get("input_context_tokens")
    input_context_text = record.get("input_context_text")

    if input_context_tokens is not None and input_context_text is not None:
        raise SystemExit(
            f"{path}:{line_number}: use either input_context_tokens or input_context_text, not both"
        )

    if input_context_tokens is not None:
        if (
            not isinstance(input_context_tokens, int)
            or isinstance(input_context_tokens, bool)
            or input_context_tokens < 0
        ):
            raise SystemExit(f"{path}:{line_number}: input_context_tokens must be a non-negative integer")

    if input_context_text is not None and not isinstance(input_context_text, str):
        raise SystemExit(f"{path}:{line_number}: input_context_text must be a string")

    values["input_context_tokens"] = input_context_tokens
    values["input_context_text"] = input_context_text
    return Sample(**values)


def exact_counter(encoding_name: str) -> Callable[[str], int]:
    try:
        import tiktoken  # type: ignore[import-not-found]
    except ImportError as exc:
        raise SystemExit(
            "Exact benchmark mode requires tiktoken. Install it in this Python environment "
            "with: python -m pip install tiktoken\n"
            "For a non-exact smoke test, rerun with --approx."
        ) from exc

    try:
        encoding = tiktoken.get_encoding(encoding_name)
    except Exception as exc:
        raise SystemExit(f"Could not load tiktoken encoding '{encoding_name}': {exc}") from exc

    return lambda text: len(encoding.encode(text))


def approximate_counter(text: str) -> int:
    tokens = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
    return max(len(tokens), 1 if text else 0)


def count_samples(samples: list[Sample], counter: Callable[[str], int]) -> list[CountedSample]:
    counted: list[CountedSample] = []
    for sample in samples:
        if sample.input_context_tokens is not None:
            context_tokens = sample.input_context_tokens
        elif sample.input_context_text:
            context_tokens = counter(sample.input_context_text)
        else:
            context_tokens = 0

        counted.append(
            CountedSample(
                sample=sample,
                normal_tokens=counter(sample.normal_output),
                analphacodex_tokens=counter(sample.analphacodex_output),
                context_tokens=context_tokens,
            )
        )

    return counted


def format_report(counted: list[CountedSample], measurement: str, details: bool) -> str:
    normal_total = sum(item.normal_tokens for item in counted)
    analphacodex_total = sum(item.analphacodex_tokens for item in counted)
    context_total = sum(item.context_tokens for item in counted)
    saved_total = normal_total - analphacodex_total
    output_reduction = 0.0 if normal_total == 0 else (saved_total / normal_total) * 100
    normal_run_total = context_total + normal_total
    analphacodex_run_total = context_total + analphacodex_total
    run_reduction = 0.0 if normal_run_total == 0 else (saved_total / normal_run_total) * 100

    lines = [
        "analpha benchmark:",
        f"- measurement: {measurement}",
        f"- samples: {len(counted)}",
        f"- input/context tokens: {context_total}",
        f"- normal output tokens: {normal_total}",
        f"- analpha output tokens: {analphacodex_total}",
        f"- output tokens saved for sample set: {saved_total}",
        f"- output reduction for sample set: {output_reduction:.1f}%",
    ]

    if context_total:
        lines.extend(
            [
                f"- normal total run tokens: {normal_run_total}",
                f"- analpha total run tokens: {analphacodex_run_total}",
                f"- total run reduction with provided context: {run_reduction:.1f}%",
            ]
        )

    if details:
        lines.append("")
        lines.append("details:")
        for index, item in enumerate(counted, start=1):
            lines.append(
                f"{index}. {item.sample.mode}: context={item.context_tokens}, "
                f"normal_output={item.normal_tokens}, analpha_output={item.analphacodex_tokens}, "
                f"output_saved={item.saved_tokens}"
            )

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare known normal outputs with known analpha outputs."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"JSONL benchmark file. Default: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "--encoding",
        default="o200k_base",
        help="tiktoken encoding for exact counts. Default: o200k_base.",
    )
    parser.add_argument(
        "--approx",
        action="store_true",
        help="Use rough regex counts instead of exact tiktoken counts.",
    )
    parser.add_argument("--details", action="store_true", help="Show per-sample counts.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    samples = load_samples(args.input)

    if args.approx:
        counter = approximate_counter
        measurement = "approximate regex count, not tokenizer-accurate"
    else:
        counter = exact_counter(args.encoding)
        measurement = f"exact tiktoken encoding {args.encoding}"

    counted = count_samples(samples, counter)
    print(format_report(counted, measurement, args.details))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
