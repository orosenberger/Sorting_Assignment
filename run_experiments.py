import sys
import time
import random
import argparse
import numpy as np
import matplotlib.pyplot as plt


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = random.randint(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        pi = i + 1
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)


ALGO_NAMES = {1: "Bubble Sort", 2: "Selection Sort", 3: "Insertion Sort", 4: "Merge Sort", 5: "Quick Sort"}
ALGO_FUNCS = {1: bubble_sort, 2: selection_sort, 3: insertion_sort, 4: merge_sort, 5: quick_sort}


def get_test_array(size, exp_type):
    if exp_type == 1:
        return [random.randint(0, 10000) for _ in range(size)]
    arr = list(range(size))
    noise_levels = {2: 0.15}
    noise = noise_levels[exp_type]
    num_swaps = int(size * noise)
    for _ in range(num_swaps):
        i, j = random.randint(0, size - 1), random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', nargs='+', type=int, required=True)
    parser.add_argument('-s', nargs='+', type=int, required=True)
    parser.add_argument('-e', type=int, default=1)
    parser.add_argument('-r', type=int, default=5)
    args = parser.parse_args()

    sys.setrecursionlimit(max(args.s) * 3 + 1000)

    for algo_id in args.a:
        if algo_id not in ALGO_FUNCS:
            print(f"Unknown algorithm ID: {algo_id}")
            return

    all_results = {}

    for algo_id in args.a:
        name = ALGO_NAMES[algo_id]
        func = ALGO_FUNCS[algo_id]
        means = []
        stds = []

        for size in args.s:
            times = []
            for rep in range(args.r):
                data = get_test_array(size, args.e)
                start = time.perf_counter()
                func(data)
                elapsed = time.perf_counter() - start
                times.append(elapsed)

            means.append(np.mean(times))
            stds.append(np.std(times))

        all_results[name] = (means, stds)

    plt.figure(figsize=(10, 6))

    titles = {
        1: "Runtime Comparison (Random Arrays)",
        2: "Runtime Comparison (Nearly Sorted, 15% noise)"
    }

    for name, (m, s) in all_results.items():
        plt.plot(args.s, m, label=name, marker='o', linewidth=2)
        plt.fill_between(args.s, np.array(m) - np.array(s), np.array(m) + np.array(s), alpha=0.15)

    plt.title(titles.get(args.e, "Runtime Comparison"), fontsize=14)
    plt.xlabel("Array Size (n)")
    plt.ylabel("Runtime (seconds)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    filename = "result1.png" if args.e == 1 else "result2.png"
    plt.show()


if __name__ == "__main__":
    main()
