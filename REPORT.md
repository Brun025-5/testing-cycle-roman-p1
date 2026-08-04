# Report

## Part 1

The project was forked, cloned, and set up in a virtual environment. The inherited test suite was run first, confirming that all 15 existing tests pass, and the command-line conversion was exercised manually before writing any test.

![Conversion with no test](docs/figures/part1.png "Conversion with no test")

## Part 2

Before writing new tests, the initial branch coverage of `src/roman/converter.py` was measured to establish a baseline. As expected, coverage starts at 64%, since the inherited suite only exercises the base conversion cases.

![Initial coverage](docs/figures/part2.png "Initial coverage")

## Part 3

### Control Flow Graph of _to_roman_

This section applies path testing to the `to_roman` function (lines 40 to 53 of `src/roman/converter.py`). Path testing derives a program graph from the source code, where nodes represent statements (or blocks of sequential statements) and edges represent the flow of control between them. This graph is then used to compute the cyclomatic complexity and to derive a basis set of independent paths.

Note that the _to_roman_ function is:
```python {.line-numbers}
def to_roman(n):
    if not isinstance(n, int) or isinstance(n, bool):
        raise RomanError("value must be an integer")
    if n < _MIN_VALUE:
        raise RomanError("value must be >= 1")
    if n > _MAX_VALUE:
        raise RomanError("value must be <= 3999")
    out = []
    remaining = n
    for value, symbol in _PAIRS:
        while remaining >= value:
            out.append(symbol)
            remaining -= value
    return "".join(out)

```

Each node corresponds to a statement (or a sequential block of statements) of `to_roman`, and each edge represents a possible transfer of control between them. So, the resulting CFG is:

![Control Flow Graph](docs/figures/CFG.png "Control Flow Graph"){ width=300 }

### Cyclomatic Complexity

#### DD-Path

Before computing the cyclomatic complexity, the CFG is reduced to its decision-to-decision path (DD-Path) graph. In a DD-Path graph, every maximal chain of sequential nodes (nodes with exactly one predecessor and one successor) is collapsed into a single node, so that only the decision points and junctions of the original CFG remain visible. This simplifies the counting of edges and nodes used in the cyclomatic complexity formula, while preserving the same set of possible execution paths as the original CFG.

![DD-Path](docs/figures/DD-Path.png "DD-Path"){ width=300 }

#### Computation

Thanks to the DD-Path, we can get the exact number of independent paths. The formula is:

V(G) = E - N + 2P

Where:
- E = number of edges in the control flow graph
- N = number of nodes in the control flow graph
- P = number of connected components in the control flow graph

Then, we get:

- E = 18 (edges)
- N = 14 (nodes)
- P = 1 (connected component)

Finally:

V(G) = 18 - 14 + 2*1 = 6

This means six linearly independent paths are needed to cover every decision outcome of `to_roman` at least once.

### Independent Paths

Below is a basis set of V(G) = 6 linearly independent paths through `to_roman`, each highlighted over the DD-Path graph and written as a sequence of nodes:

- Independent Path 1
![Independent Path 1](docs/figures/IP1.png "Independent Path 1"){ width=50% }

- Independent Path 2
![Independent Path 2](docs/figures/IP2.png "Independent Path 2"){ width=50% }

- Independent Path 3
![Independent Path 3](docs/figures/IP3.png  "Independent Path 3"){ width=50% }

- Independent Path 4
![Independent Path 4](docs/figures/IP4.png "Independent Path 4"){ width=50% }

- Independent Path 5
![Independent Path 5](docs/figures/IP5.png  "Independent Path 5"){ width=50% }

- Independent Path 6
![Independent Path 6](docs/figures/IP6.png  "Independent Path 6"){ width=50% }

### DU-pairs

The table below lists the definition-use pairs for each variable of `to_roman`, classifying each use as a computational use (c-use, when the variable's value is used to compute another value or is passed as an argument) or a predicate use (p-use, when the variable's value is used directly inside a decision's condition). The variable `remaining` is redefined on every iteration of the `while` loop, so the pairs created by that redefinition (9 -> 11, 9 -> 13, 13 -> 11, 13 -> 13) are included as well.

| Definition -> Use Pair (start line -> end line) | c-use     | p-use     |
|-----------------------------------------------|-----------|-----------|
| 1 -> 2                                        | n         |           |
| 1 -> 4                                        |           | n         |
| 1 -> 6                                        |           | n         |
| 1 -> 9                                        | n         |           |
| 8 -> 12                                       | out       |           |
| 8 -> 14                                       | out       |           |
| 9 -> 13                                       | remaining |           |
| 9 -> 11                                       |           | remaining |
| 10 -> 11                                      |           | value     |
| 10 -> 12                                      | symbol    |           |
| 10 -> 13                                      | value     |           |
| 12 -> 12                                      | out       |           |
| 12 -> 14                                      | out       |           |
| 13 -> 11                                      |           | remaining |
| 13 -> 13                                      | remaining |           |

### Unit Tests for Branch Coverage

Using the independent paths and the DU-pairs above as a guide, 15 new unit tests were added to `tests/test_converter.py` (the 15 inherited tests were left unmodified). The new tests target the branches that part 2 reported as missing: the three guard clauses of `to_roman` (non-integer input, boolean input, value below the minimum, value above the maximum), the guard clauses and subtractive-pair handling of `from_roman` (non-string input, empty string, invalid character, valid and invalid subtractive pairs, out-of-range totals), both outcomes of `is_valid_roman`, and the internal helpers `_count_char` and `_roundtrip_differs`.

The functions `add_roman` and `subtract_roman` were deliberately left uncovered at this stage, since they are the collaboration under test in Part 4 (integration level).

Running the coverage command again after adding the tests:

![Branch Coverage  > 85%](docs/figures/part3-13.png  "Branch Coverage  > 85%")

Branch coverage of `src/roman/converter.py` went from 64% (Part 2) to 98%, above the 85% required by this task. All 30 tests (15 inherited + 15 new) pass.