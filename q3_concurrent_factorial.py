# =============================================================
# 5022CMD Advanced Algorithms - Q3: Concurrent Processing
# Factorial calculation with and without Multithreading
# =============================================================

import threading
import time


# FACTORIAL FUNCTION  ->  Time Complexity = O(n)
def factorial(n):
    """Compute n! iteratively. Time complexity: O(n)."""
    result = 1                     # 1 operation
    for i in range(2, n + 1):      # loop runs (n - 1) times
        result = result * i        # 1 multiplication + 1 assignment each
    return result                  # 1 operation


# THREAD WORKER
def factorial_worker(n, label, results, timings):
    """Worker run by each thread: records start time, computes, records end."""
    start = time.perf_counter_ns()
    results[label] = factorial(n)
    end = time.perf_counter_ns()
    timings[label] = (start, end)


# EXPERIMENT 1: WITH MULTITHREADING
def run_with_threads(numbers):
    """
    Create one thread per factorial (50!, 100!, 200!).
    T = latest end time - earliest start time.
    """
    results = {}
    timings = {}
    threads = []

    for n in numbers:
        label = f"{n}!"
        t = threading.Thread(target=factorial_worker,
                             args=(n, label, results, timings))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    earliest_start = min(start for start, end in timings.values())
    latest_end     = max(end   for start, end in timings.values())
    elapsed = latest_end - earliest_start
    return elapsed, results


# EXPERIMENT 2: WITHOUT MULTITHREADING (sequential)
def run_without_threads(numbers):
    """Compute all factorials one after another in the main thread."""
    results = {}
    start = time.perf_counter_ns()
    for n in numbers:
        results[f"{n}!"] = factorial(n)
    end = time.perf_counter_ns()
    elapsed = end - start
    return elapsed, results


# RUN 10 ROUNDS AND REPORT
def run_experiment(numbers, rounds=10):
    print("\n" + "=" * 70)
    print(f"{'FACTORIAL EXPERIMENT: 50!, 100!, 200!':^70}")
    print("=" * 70)
    print(f"  Numbers tested : {', '.join(str(n) + '!' for n in numbers)}")
    print(f"  Rounds         : {rounds}")

    # ---- WITH multithreading ----
    print("\n" + "-" * 70)
    print("  EXPERIMENT A: WITH MULTITHREADING")
    print("-" * 70)
    print(f"  {'Round':<10}{'Time T (nanoseconds)':<25}")
    print("  " + "-" * 35)
    threaded_times = []
    for r in range(1, rounds + 1):
        elapsed, _ = run_with_threads(numbers)
        threaded_times.append(elapsed)
        print(f"  {r:<10}{elapsed:>15,} ns")
    avg_threaded = sum(threaded_times) / len(threaded_times)
    print("  " + "-" * 35)
    print(f"  {'AVERAGE':<10}{avg_threaded:>15,.1f} ns")

    # ---- WITHOUT multithreading ----
    print("\n" + "-" * 70)
    print("  EXPERIMENT B: WITHOUT MULTITHREADING (Sequential)")
    print("-" * 70)
    print(f"  {'Round':<10}{'Time T (nanoseconds)':<25}")
    print("  " + "-" * 35)
    sequential_times = []
    for r in range(1, rounds + 1):
        elapsed, _ = run_without_threads(numbers)
        sequential_times.append(elapsed)
        print(f"  {r:<10}{elapsed:>15,} ns")
    avg_sequential = sum(sequential_times) / len(sequential_times)
    print("  " + "-" * 35)
    print(f"  {'AVERAGE':<10}{avg_sequential:>15,.1f} ns")

    # ---- SUMMARY ----
    print("\n" + "=" * 70)
    print(f"{'SUMMARY':^70}")
    print("=" * 70)
    print(f"  Average WITH multithreading    : {avg_threaded:>15,.1f} ns")
    print(f"  Average WITHOUT multithreading : {avg_sequential:>15,.1f} ns")
    diff = avg_threaded - avg_sequential
    if diff > 0:
        print(f"  Multithreading was SLOWER by   : {diff:>15,.1f} ns")
    else:
        print(f"  Multithreading was FASTER by   : {abs(diff):>15,.1f} ns")
    print("=" * 70)


# DEMONSTRATE FACTORIAL OUTPUT (verify correctness)
def show_factorial_values(numbers):
    print("\n  Computed factorial values (digit count shown):")
    for n in numbers:
        val = factorial(n)
        print(f"   {n}! = {len(str(val))} digits "
              f"(starts with {str(val)[:10]}...)")


# ENTRY POINT
if __name__ == "__main__":
    NUMBERS = [50, 100, 200]
    show_factorial_values(NUMBERS)
    run_experiment(NUMBERS, rounds=10)