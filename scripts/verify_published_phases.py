"""把 ephem 算出的月相时刻和外部公开时刻表对表。

这是 tonight-sky 里第一个"判据不在我自己手里"的检查：期望值来自
lunaf.com 的 2026 年公开月相表（tests/data/moon_phases_2026_lunaf.json，
UTC，精确到分钟），不是我自己的断言。

用法：uv run --with ephem python scripts/verify_published_phases.py
"""
from __future__ import annotations

import json
import os
import statistics
from typing import Dict, List

import ephem

DATA = os.path.join(os.path.dirname(__file__), "..", "tests", "data",
                    "moon_phases_2026_lunaf.json")

NEXT_FN = {
    "New Moon": ephem.next_new_moon,
    "First Quarter": ephem.next_first_quarter_moon,
    "Full Moon": ephem.next_full_moon,
    "Last Quarter": ephem.next_last_quarter_moon,
}


def load_published() -> List[Dict[str, str]]:
    with open(DATA, encoding="utf-8") as fh:
        raw = json.load(fh)
    return [{"date": d, "time": t, "phase": p} for d, t, p in raw["phases"]]


def nearest_phase(published_utc: str, phase: str) -> float:
    """返回 ephem 与该公开时刻的绝对误差（秒）。"""
    target = ephem.Date(published_utc)
    guess = NEXT_FN[phase](ephem.Date(ephem.Date(published_utc) - 2.0))
    # 若落点差太远（跨月边界），往后多找一次
    if abs(float(guess) - float(target)) > 1.5:
        guess = NEXT_FN[phase](ephem.Date(float(target) - 0.5))
    return abs(float(guess) - float(target)) * 86400.0


def check() -> Dict[str, object]:
    rows = []
    for rec in load_published():
        stamp = f"{rec['date']} {rec['time']}:00"
        rows.append({**rec, "error_s": round(nearest_phase(stamp, rec["phase"]), 2)})
    errs = [r["error_s"] for r in rows]
    worst = max(rows, key=lambda r: r["error_s"])
    return {
        "n": len(rows),
        "max_s": max(errs),
        "median_s": round(statistics.median(errs), 2),
        "mean_s": round(statistics.mean(errs), 2),
        "worst": worst,
        "rows": rows,
    }


def main() -> None:
    res = check()
    print(f"外部锚点 {res['n']} 条（lunaf.com 2026 月相表，UTC，分钟精度）")
    print(f"最大误差 {res['max_s']:.1f}s · 中位 {res['median_s']:.1f}s · 平均 {res['mean_s']:.1f}s")
    w = res["worst"]
    print(f"最差：{w['date']} {w['time']} {w['phase']} → {w['error_s']:.1f}s")
    over = [r for r in res["rows"] if r["error_s"] > 60]
    print(f"超过 60s 的条目：{len(over)}")
    for r in over:
        print("  ", r["date"], r["time"], r["phase"], f"{r['error_s']}s")


if __name__ == "__main__":
    main()
