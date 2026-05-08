#!/usr/bin/env python3
"""Manual estimated stats for the analpha skill."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


BASELINE_TOKENS = 60
ACTUAL_TOKENS = {
    ("smart", False): 2,
    ("smart", True): 20,
    ("emoji", False): 2,
    ("emoji", True): 2,
    ("ultra", False): 1,
    ("ultra", True): 1,
}

DEFAULT_STATS: dict[str, int] = {
    "total_replies": 0,
    "smart_replies": 0,
    "emoji_replies": 0,
    "ultra_replies": 0,
    "smart_explanations": 0,
    "estimated_baseline_reply_tokens": BASELINE_TOKENS,
    "estimated_actual_reply_tokens": 0,
    "estimated_tokens_saved": 0,
}


def stats_path() -> Path:
    return Path(__file__).resolve().parents[1] / "analphacodex_stats.json"


def load_stats(path: Path) -> dict[str, Any]:
    if not path.exists():
        return dict(DEFAULT_STATS)

    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        loaded = {}

    stats = dict(DEFAULT_STATS)
    for key, value in loaded.items():
        if key in stats and isinstance(value, int):
            stats[key] = value
    return stats


def save_stats(path: Path, stats: dict[str, Any]) -> None:
    path.write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def recalculate(stats: dict[str, Any]) -> dict[str, Any]:
    total = int(stats["total_replies"])
    actual = int(stats["estimated_actual_reply_tokens"])
    baseline = total * BASELINE_TOKENS
    stats["estimated_tokens_saved"] = max(baseline - actual, 0)
    return stats


def record(mode: str, explanation: bool, count: int) -> dict[str, Any]:
    path = stats_path()
    stats = load_stats(path)
    actual_tokens = ACTUAL_TOKENS[(mode, explanation)] * count

    stats["total_replies"] += count
    stats[f"{mode}_replies"] += count

    if mode == "smart" and explanation:
        stats["smart_explanations"] += count

    stats["estimated_actual_reply_tokens"] += actual_tokens
    recalculate(stats)
    save_stats(path, stats)
    return stats


def reset() -> dict[str, Any]:
    path = stats_path()
    stats = dict(DEFAULT_STATS)
    save_stats(path, stats)
    return stats


def format_stats(stats: dict[str, Any]) -> str:
    total = int(stats["total_replies"])
    saved = int(stats["estimated_tokens_saved"])
    baseline = total * BASELINE_TOKENS
    percent = 0.0 if baseline == 0 else (saved / baseline) * 100

    return "\n".join(
        [
            "analpha manual estimated stats:",
            f"- recorded replies: {total}",
            f"- smart: {stats['smart_replies']}",
            f"- emoji: {stats['emoji_replies']}",
            f"- ultra: {stats['ultra_replies']}",
            f"- smart explanations: {stats['smart_explanations']}",
            f"- assumed baseline tokens: {baseline}",
            f"- estimated analphacodex tokens: {stats['estimated_actual_reply_tokens']}",
            f"- estimated tokens saved vs baseline: {saved}",
            f"- estimated reduction vs baseline: {percent:.1f}%",
            "Note: manual counter only; not automatic telemetry or exact tokenizer measurement.",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track manual estimated analpha token savings.")
    subparsers = parser.add_subparsers(dest="command")

    record_parser = subparsers.add_parser("record", help="Record one or more estimated replies.")
    record_parser.add_argument("--mode", choices=["smart", "emoji", "ultra"], required=True)
    record_parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of replies to record. Default: 1.",
    )
    record_parser.add_argument(
        "--explanation",
        action="store_true",
        help="Mark a smart-mode short explanation reply.",
    )

    subparsers.add_parser("reset", help="Reset local estimated stats.")
    subparsers.add_parser("show", help="Show local estimated stats.")
    subparsers.add_parser("path", help="Show the local stats file path.")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "record":
        if args.count < 1:
            raise SystemExit("--count must be 1 or greater")
        stats = record(args.mode, args.explanation, args.count)
    elif args.command == "reset":
        stats = reset()
    elif args.command == "path":
        print(stats_path())
        return 0
    else:
        stats = recalculate(load_stats(stats_path()))

    print(format_stats(stats))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
