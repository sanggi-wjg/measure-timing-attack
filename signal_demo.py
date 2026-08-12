import hmac
import random
import statistics
import time

import matplotlib.pyplot as plt

from main import SECRET


plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

# 한 샘플당 비교 반복 횟수 (신호를 타이머 해상도 위로 증폭)
AMPLIFY = 10_000
# 조건당 타이밍 샘플 수 (박스 하나를 이루는 점 개수)
SAMPLES = 200

PREFIX_LENGTHS = [100, 400, 700, 1000]

OUTPUT_PATH = "signal.png"


def make_request(prefix_len: int) -> str:
    return SECRET[:prefix_len] + "*" * (len(SECRET) - prefix_len)


def measure_compare(request_value: str) -> float:
    secret = SECRET
    hits = 0
    start = time.perf_counter_ns()
    for _ in range(AMPLIFY):
        hits += request_value == secret
    end = time.perf_counter_ns()
    return (end - start) / AMPLIFY


def measure_compare_digest(request_value: str) -> float:
    secret = SECRET
    hits = 0
    start = time.perf_counter_ns()
    for _ in range(AMPLIFY):
        hits += hmac.compare_digest(request_value, secret)
    end = time.perf_counter_ns()
    return (end - start) / AMPLIFY


MEASURERS = {
    "compare (==)": measure_compare,
    "compare_digest (hmac)": measure_compare_digest,
}

TITLES = {
    "compare (==)": "compare (== 비교, 조기 종료)",
    "compare_digest (hmac)": "compare_digest (상수 시간)",
}


def collect_interleaved() -> dict[str, dict[int, list[float]]]:
    request_values = {p: make_request(p) for p in PREFIX_LENGTHS}
    conditions = [(label, p) for label in MEASURERS for p in PREFIX_LENGTHS]

    for label, prefix_len in conditions:
        MEASURERS[label](request_values[prefix_len])

    results: dict[str, dict[int, list[float]]] = {
        label: {p: [] for p in PREFIX_LENGTHS} for label in MEASURERS
    }

    for _ in range(SAMPLES):
        random.shuffle(conditions)
        for label, prefix_len in conditions:
            per_op = MEASURERS[label](request_values[prefix_len])
            results[label][prefix_len].append(per_op)

    return results


def print_summary(results: dict[str, dict[int, list[float]]]) -> None:
    for label, by_prefix in results.items():
        print(label)
        for prefix_len in PREFIX_LENGTHS:
            samples = by_prefix[prefix_len]
            print(
                f"  prefix_len={prefix_len:>4}  "
                f"min={min(samples):>6.1f}  median={statistics.median(samples):>6.1f} ns/op"
            )


def plot_stats(results: dict[str, dict[int, list[float]]]) -> None:
    fig, axes = plt.subplots(1, len(results), figsize=(12, 5))

    for ax, (label, by_prefix) in zip(axes, results.items()):
        data = [by_prefix[prefix_len] for prefix_len in PREFIX_LENGTHS]
        ax.boxplot(
            data,
            tick_labels=[str(p) for p in PREFIX_LENGTHS],
            showmeans=True,
            showfliers=False,
        )
        ax.set_title(TITLES.get(label, label))
        ax.set_xlabel("prefix_len (정답 문자 수)")
        ax.set_ylabel("비교 1회당 시간 (ns)")
        ax.grid(True, axis="y", alpha=0.3)

    fig.suptitle(
        f"비교시간 (증폭={AMPLIFY}, 박스당 {SAMPLES}샘플, 순서 섞음)"
    )
    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=150)
    print(f"saved: {OUTPUT_PATH}")


def main():
    results = collect_interleaved()
    print_summary(results)
    plot_stats(results)


if __name__ == "__main__":
    main()