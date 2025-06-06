# Concepts of Data Science: Ternary Search Tree

This project implements a Ternary Search Tree (TST) as part of the `Concepts of Data Science` course at UHasselt (2024–2025). It includes:

- an object-oriented Python implementation of a TST;
- comprehensive unit tests;
- benchmarking tools designed to run on the KU Leuven HPC infrastructure;
- performance analysis across best-case, average-case, and worst-case scenarios.

The goal is to understand, implement, and empirically evaluate the efficiency of TSTs for string storage and retrieval.

## Software Requirements

Python 3.10 or above is required to run the project code. A `conda` installation is also recommended - we used it throughout the project as Python's package and environment manager.

The main TST implementation and tests use only Python's standard library. However, the benchmarking code depends on:

- `matplotlib` for plotting;
- `numpy` for numerical operations.

You can install them using:

```bash
conda install matplotlib numpy
```

## Contents

### Ternary Search Tree

The core TST implementation is in `src/ternary_search_tree.py`. Key methods include:

- `insert(term: str)`: adds a word to the tree, character by character;
- `search(term: str, exact: bool = False)`: checks if a word or prefix exists in the tree;
- `__len__()`: counts how many strings are stored in the tree;
- `__repr__()`: visualizes the structure of the tree;
- `all_strings()`: retrieves all stored strings.

#### Expected Time Complexity

Each operation in a Ternary Search Tree (TST) proceeds character-by-character through the input string.

At each character level, it compares the character against the current node and follows `<`, `=`, or `>` links, which act like a binary search among characters. This makes the structure similar to a hybrid of a [trie](https://en.wikipedia.org/wiki/Trie) and a binary search tree.

| Operation     | Best Case | Average Case | Worst Case | Explanation                                                                                     |
| ------------- | --------- | ------------ | ---------- | ----------------------------------------------------------------------------------------------- |
| `insert`      | O(n)      | O(n log k)   | O(n²)      | One character processed per level; `log k` factor comes from balanced comparison at each level. |
| `search`      | O(n)      | O(n log k)   | O(n²)      | Same reasoning as `insert`; worse with degenerate trees (e.g. sorted input).                    |
| `__len__`     | O(N)      | O(N)         | O(N)       | Traverses all nodes to count terminators.                                                       |
| `all_strings` | O(N + kL) | O(N + kL)    | O(N + kL)  | Full traversal + reconstruction of `k` strings of length `L`.                                   |

, where:

- `n` = length of the word;
- `k` = number of stored strings;
- `L` = average string length;
- `N` = total number of nodes.

**Comparison to Binary Search Trees (BSTs):**

- In a traditional BST storing full strings, comparison is `O(n)` per node because full string comparisons are used;
- In a TST, comparisons are `O(1)` per node (just characters), but the number of nodes per word is `n`;
- So both BST and TST have worst-case `O(n log k)` time, but TST often uses less memory and can perform prefix queries more naturally.

#### Expected Space Complexity

| Operation     | Space Complexity | Explanation                                          |
| ------------- | ---------------- | ---------------------------------------------------- |
| `insert`      | O(n)             | Up to `n` new nodes per inserted word.               |
| `search`      | O(n)             | Stack usage during recursive descent.                |
| `__len__`     | O(H)             | Depth-first traversal stack.                         |
| `__repr__`    | O(N)             | Builds a list of lines representing the entire tree. |
| `all_strings` | O(kL + H)        | Output list + recursion stack.                       |

, where `H` = height of the tree (can be up to `n` per word).

TSTs support prefix search more naturally than BSTs.

### Testing

Unit tests are located in `src/tests/test_ternary_search_tree.py`. They validate:

- correctness of `insert`, `search`, `all_strings`, and `__len__`;
- edge cases like the empty string;
- behavior on overlapping prefixes.

To run all tests:

```bash
python -m unittest discover -s src/tests
```

## Contributors

This project was developed as part of a team assignment. Collaboration, code contributions, and commit history are documented in the GitHub repository.
