import math
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import timeit

from functools import wraps

from src.ternary_search_tree import TernarySearchTree

DEFAULT_STEPS = 10
BENCHMARK_RESULTS_DIRECTORY = "benchmark_results"


def generate_individual_plot(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        results: dict[int, list[int]] = func(*args, **kwargs)

        try:
            # define plot space
            (_, ax) = plt.subplots(figsize=(10, 6))

            # define plot title and axes labels
            ax.set(
                title=func.__name__,
                xlabel="input size (# words)",
                ylabel="mean execution time (s)",
            )

            # add plot gridlines
            plt.grid()

            # plot results
            plt.plot(
                list(results.keys()),
                [sum(result) / len(result) for result in results.values()],
            )

            # save plot to file (with timestamp)
            current_time = timeit.default_timer()
            filename = os.path.join(
                BENCHMARK_RESULTS_DIRECTORY,
                f"{func.__name__}_{current_time}.png"
            )
            os.makedirs(BENCHMARK_RESULTS_DIRECTORY, exist_ok=True)
            plt.savefig(filename)
        except Exception:
            print(f"unable to create plot for {func.__name__}")

        return results

    return wrap


def generate_aggregate_plot(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        results: dict[str, dict[int, list[int]]] = func(*args, **kwargs)

        try:
            # define plot space
            (_, ax) = plt.subplots(figsize=(10, 6))

            # define plot title and axes labels
            ax.set(
                title=func.__name__,
                xlabel="input size (# words)",
                ylabel="mean execution time (s)",
            )

            # add plot gridlines
            plt.grid()

            # plot one line per case
            for case, timings in results.items():
                input_sizes = sorted(timings.keys())
                mean_times = [
                    sum(timings[size]) / len(timings[size])
                    for size in input_sizes
                ]

                plt.plot(input_sizes, mean_times, label=case)

            # add legend
            plt.legend()

            # save plot to file (with timestamp)
            current_time = timeit.default_timer()
            filename = os.path.join(
                BENCHMARK_RESULTS_DIRECTORY,
                f"{func.__name__}_{current_time}.png"
            )
            os.makedirs(BENCHMARK_RESULTS_DIRECTORY, exist_ok=True)
            plt.savefig(filename)
        except Exception:
            print(f"unable to create plot for {func.__name__}")

        return results

    return wrap


class Timer:
    def __init__(self, method: str, size: int, results: list[float]) -> None:
        self.method = method
        self.size = size
        self.results = results
        self.tree = TernarySearchTree()

    def __enter__(self) -> TernarySearchTree:
        self.start_time = timeit.default_timer()
        return self.tree

    def __exit__(self, type, value, traceback) -> None:
        self.end_time = timeit.default_timer()

        # calculate and print time difference
        time_difference = self.end_time - self.start_time
        self.results.append(time_difference)
        print(f"`{self.method}` ({self.size}) took: {time_difference}s")


class BenchmarkTernaryTestTree:
    def __init__(self, *args, **kwargs) -> None:
        with open("data/search_trees/corncob_lowercase.txt") as file:
            words = [line.strip() for line in file]

        # sorted words
        self.sorted_words = sorted(words)
        self.sorted_populated_tree = TernarySearchTree()
        for word in self.sorted_words:
            self.sorted_populated_tree.insert(word)

        # shuffled words
        self.shuffled_words = words.copy()
        random.shuffle(self.shuffled_words)
        self.shuffled_populated_tree = TernarySearchTree()
        for word in self.shuffled_words:
            self.shuffled_populated_tree.insert(word)

        # median ordered words
        self.median_ordered_words = self._median_order(words)
        self.median_populated_tree = TernarySearchTree()
        for word in self.median_ordered_words:
            self.median_populated_tree.insert(word)

    @classmethod
    def _median_order(cls, words: list[str]) -> list[str]:
        if not words:
            return []

        mid = len(words) // 2
        return (
            [words[mid]]
            + cls._median_order(words[:mid])
            + cls._median_order(words[mid + 1:])
        )

    @generate_individual_plot
    def insert_best_case(
        self,
        steps: int = DEFAULT_STEPS
    ) -> dict[int, list[int]]:
        results = {}

        # words should be in median order for best-case performance
        # balanced tree
        limit = math.log10(len(self.median_ordered_words))
        sizes = np.logspace(1, limit, steps)

        for size in sizes:
            words = self.median_ordered_words[:int(size)]
            sample_results = results[len(words)] = []

            for _ in range(steps):
                with Timer(
                    "insert_best_case",
                    int(size), sample_results
                ) as tree:
                    for word in words:
                        tree.insert(word)

        return results

    @generate_individual_plot
    def insert_average_case(
        self,
        steps: int = DEFAULT_STEPS
    ) -> dict[int, list[int]]:
        results = {}

        # words should be in random order for average-case performance
        limit = math.log10(len(self.shuffled_words))
        sizes = np.logspace(1, limit, steps)

        for size in sizes:
            words = self.shuffled_words[:int(size)]
            sample_results = results[len(words)] = []

            for _ in range(steps):
                with Timer(
                    "insert_average_case",
                    int(size), sample_results
                ) as tree:
                    for word in words:
                        tree.insert(word)

        return results

    @generate_individual_plot
    def insert_worst_case(
        self,
        steps: int = DEFAULT_STEPS
    ) -> dict[int, list[int]]:
        results = {}

        # words should be sorted alphabetically for worst-case performance
        # unbalanced tree
        limit = math.log10(len(self.sorted_words))
        sizes = np.logspace(1, limit, steps)

        for size in sizes:
            words = self.sorted_words[:int(size)]
            sample_results = results[len(words)] = []

            for _ in range(steps):
                with Timer(
                    "insert_worst_case",
                    int(size), sample_results
                ) as tree:
                    for word in words:
                        tree.insert(word)

        return results

    @generate_aggregate_plot
    def insert_all_cases(
        self, steps: int = DEFAULT_STEPS
    ) -> dict[str, dict[int, list[int]]]:
        results = {"best": {}, "average": {}, "worst": {}}

        cases = {
            "best": self.median_ordered_words,
            "average": self.shuffled_words,
            "worst": self.sorted_words,
        }

        # words should be in median order for best-case performance
        limit = math.log10(len(self.median_ordered_words))
        sizes = np.logspace(1, limit, steps)

        for case in cases:
            for size in sizes:
                words = cases[case][:int(size)]
                sample_results = results[case][len(words)] = []

                for _ in range(steps):
                    with Timer(
                        f"insert_{case}_case", int(size), sample_results
                    ) as tree:
                        for word in words:
                            tree.insert(word)

        return results

    @generate_individual_plot
    def search_best_case(
        self,
        steps: int = DEFAULT_STEPS
    ) -> dict[int, list[int]]:
        results = {}

        limit = math.log10(len(self.sorted_words))
        sizes = np.logspace(1, limit, steps)

        for size in sizes:
            words = self.sorted_words[:int(size)]
            sample_results = results[len(words)] = []

            # words should be in median order for best-case performance
            # balanced tree
            for _ in range(steps):
                with Timer("search_best_case", int(size), sample_results):
                    for word in words:
                        self.median_populated_tree.search(word)

        return results

    @generate_individual_plot
    def search_average_case(
        self,
        steps: int = DEFAULT_STEPS
    ) -> dict[int, list[int]]:
        results = {}

        limit = math.log10(len(self.sorted_words))
        sizes = np.logspace(1, limit, steps)

        for size in sizes:
            words = self.sorted_words[:int(size)]
            sample_results = results[len(words)] = []

            # words should be in random order for average-case performance
            for _ in range(steps):
                with Timer("search_best_case", int(size), sample_results):
                    for word in words:
                        self.shuffled_populated_tree.search(word)

        return results

    @generate_individual_plot
    def search_worst_case(
        self,
        steps: int = DEFAULT_STEPS
    ) -> dict[int, list[int]]:
        results = {}

        limit = math.log10(len(self.sorted_words))
        sizes = np.logspace(1, limit, steps)

        for size in sizes:
            words = self.sorted_words[:int(size)]
            sample_results = results[len(words)] = []

            # words should be sorted alphabetically for worst-case performance
            # unbalanced tree
            for _ in range(steps):
                with Timer("search_best_case", int(size), sample_results):
                    for word in words:
                        self.sorted_populated_tree.search(word)

        return results

    @generate_aggregate_plot
    def search_all_cases(
        self, steps: int = DEFAULT_STEPS
    ) -> dict[str, dict[int, list[int]]]:
        results = {"best": {}, "average": {}, "worst": {}}

        cases: dict[str, TernarySearchTree] = {
            "best": self.median_populated_tree,
            "average": self.shuffled_populated_tree,
            "worst": self.sorted_populated_tree,
        }

        limit = math.log10(len(self.sorted_words))
        sizes = np.logspace(1, limit, steps)

        for case in cases:
            for size in sizes:
                words = self.sorted_words[:int(size)]
                sample_results = results[case][len(words)] = []

                for _ in range(steps):
                    with Timer(
                        f"search_{case}_case", int(size), sample_results
                    ):
                        for word in words:
                            cases[case].search(word)

        return results


benchmark = BenchmarkTernaryTestTree()

if __name__ == "__main__":
    benchmark.insert_all_cases()
    benchmark.search_all_cases()
