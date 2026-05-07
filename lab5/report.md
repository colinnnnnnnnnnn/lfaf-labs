# Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Author: Poiata Calin

----

## Theory

Chomsky Normal Form (CNF) is a restricted, normalized form for context-free grammars where every production must have one of these canonical forms:

* $A \rightarrow BC$, where $A, B, C$ are nonterminals (binary branching);
* $A \rightarrow a$, where $a$ is a terminal symbol (terminal production).

In some theoretical definitions, $S \rightarrow \varepsilon$ is also allowed only in special cases when the start symbol derives the empty string. For this laboratory, epsilon productions are eliminated entirely as requested by the variant normalization steps.

### Why Chomsky Normal Form?

CNF plays a crucial role in formal language theory and practical applications:

1. **Theoretical Significance**: CNF is one of the most important normal forms for context-free grammars, proposed by Noam Chomsky. Every context-free grammar that does not generate the empty language can be converted to CNF while preserving its language.

2. **CYK Algorithm**: The Cocke–Younger–Kasami (CYK) parsing algorithm requires grammars to be in CNF. This algorithm solves the membership problem in polynomial time $O(n^3)$, where $n$ is the length of the input string.

3. **Proof Simplification**: Many theorems about context-free languages are easier to prove when the grammar is in CNF, because productions have a predictable structure.

4. **Computational Simplicity**: Binary productions eliminate the need to consider productions of arbitrary length, making parsing and analysis more straightforward.

### Normalization Process

Converting an arbitrary context-free grammar to CNF requires a systematic transformation pipeline:

* Epsilon productions must be eliminated.
* Unit productions (where the RHS is a single nonterminal) must be removed.
* Inaccessible symbols (not reachable from the start symbol) must be pruned.
* Non-productive symbols (that cannot derive terminal strings) must be removed.
* All remaining productions must be rewritten to use only binary branching and terminal symbols.


## Objectives

* Learn the CNF constraints and normalization workflow.
* Implement in Python a reusable method for grammar normalization.
* Apply the complete transformation pipeline to the assigned variant.
* Verify that the resulting grammar is valid CNF.
* Support generic input grammars through a text file interface (bonus).


## Variant 21

The assigned grammar is:

* $V_N=\{S,A,B,C,D\}$ (nonterminals)
* $V_T=\{a,b,d\}$ (terminals)
* Start symbol: $S$
* Productions:
  * $S \rightarrow dB$
  * $S \rightarrow AC$
  * $A \rightarrow d$
  * $A \rightarrow dS$
  * $A \rightarrow aBdB$
  * $B \rightarrow a$
  * $B \rightarrow aA$
  * $B \rightarrow AC$
  * $D \rightarrow ab$
  * $C \rightarrow bC$
  * $C \rightarrow \varepsilon$

### Initial Grammar Analysis

Observations about the initial grammar:

* The nonterminal $C$ has an epsilon production, which violates CNF.
* The production $B \rightarrow AC$ is a unit production in some contexts after epsilon removal.
* The production $A \rightarrow aBdB$ has 4 symbols, which violates the binary constraint of CNF.
* The nonterminal $D$ is not reachable from the start symbol $S$, making it inaccessible.

### Required Transformation Steps

1. **Eliminate epsilon productions**: Remove $C \rightarrow \varepsilon$ and add derived productions for all nullable nonterminals.
2. **Eliminate unit (renaming) productions**: Remove single-nonterminal productions like $S \rightarrow A$ and $B \rightarrow A$.
3. **Eliminate inaccessible symbols**: Remove nonterminals that cannot be reached from $S$.
4. **Eliminate non-productive symbols**: Remove nonterminals that cannot derive terminal strings.
5. **Obtain CNF**: Rewrite all productions into the two allowed forms and introduce helper nonterminals.


## Implementation Description

### General Idea

The solution is split into two main files:

* **`cnf_grammar.py`** contains a reusable `CFG` (Context-Free Grammar) class and all transformation methods. This module is designed to be independent of any specific variant and can process any context-free grammar.
* **`main.py`** provides the entry point: it loads a grammar from a text file, runs every normalization stage sequentially, and prints the intermediate results after each transformation for verification.
* **`variant21_grammar.txt`** contains the specific grammar for Variant 21 in a standardized text format.

The architecture supports flexibility:

* Default input is `variant21_grammar.txt` when no arguments are provided.
* Another grammar can be loaded using the `--input` or `-i` command-line flag.
* The CFG class can be imported and used by other Python modules.


### Grammar Representation

The `CFG` class uses a dataclass structure with the following fields:

* **`nonterminals: set[str]`** — a set of all nonterminal symbols.
* **`terminals: set[str]`** — a set of all terminal symbols.
* **`start_symbol: str`** — the distinguished start symbol.
* **`productions: dict[str, set[tuple[str, ...]]]`** — a mapping from each nonterminal to the set of its possible right-hand sides.

Key design decisions:

* Each right-hand side (RHS) is stored as a tuple of symbols, which is immutable and hashable.
* Multiple RHS for the same nonterminal are stored in a set, automatically deduplicating them.
* Epsilon (empty production) is represented as an empty tuple `()`, not as a special epsilon symbol.
* This representation allows efficient queries like "is symbol $X$ reachable?" or "which nonterminals are productive?"

Example representation:

The production $A \rightarrow aBdB | d | dS$ is stored as:

```python
"A": {("a", "B", "d", "B"), ("d",), ("d", "S")}
```


### Parsing Input Grammar

The function `load_grammar_from_file()` reads grammar files in a human-readable text format:

```text
VN=S,A,B,C,D
VT=a,b,d
S=S
P:
S->dB
S->AC
A->d
A->dS
A->aBdB
B->a
B->aA
B->AC
D->ab
C->bC
C->ε
```

File format details:

* Line 1: `VN=...` lists all nonterminals separated by commas.
* Line 2: `VT=...` lists all terminals separated by commas.
* Line 3: `S=...` specifies the start symbol.
* Lines 4+: Production rules in the form `Nonterminal->RHS` or `Nonterminal->RHS1|RHS2|...`.

Flexibility and robustness:

* Empty lines and lines starting with `#` are automatically ignored.
* The header line `P:` is optional.
* Epsilon can be written in multiple ways: `ε`, `eps`, `epsilon`, or just an empty RHS.
* Symbols in RHS can be concatenated directly (e.g., `aBdB`) or space-separated (e.g., `a B d B`).
* The parser validates that all symbols in rules are declared in VN or VT, raising errors for unknown symbols.

This format is both human-friendly and machine-parseable.


### Transformation Methods

The `CFG` class implements each required transformation:

#### `eliminate_epsilon_productions()`

This method removes all epsilon productions while preserving the language of the grammar.

**Algorithm:**

1. Compute the set of **nullable nonterminals** — those that can derive $\varepsilon$ either directly or through a chain of nullable symbols. This is done iteratively: if a production $A \rightarrow B_1 B_2 \ldots B_k$ has all RHS symbols nullable, then $A$ is also nullable.
2. For each production $A \rightarrow \alpha_1 \alpha_2 \ldots \alpha_n$, generate all combinations by selectively removing nullable symbols from the RHS. This ensures that any derivation producing $\varepsilon$ is captured by the new productions.
3. Remove explicit epsilon productions ($A \rightarrow \varepsilon$) from the grammar.

**Example from Variant 21:**

* Initially, $C$ is nullable (via $C \rightarrow \varepsilon$).
* The production $S \rightarrow AC$ generates $S \rightarrow A$ and $S \rightarrow C$ (by removing nullable $C$ and then $A$).
* The production $B \rightarrow AC$ generates $B \rightarrow A$, $B \rightarrow C$, and $B \rightarrow \text{(nothing)}$, but $(\text{nothing})$ is discarded.

#### `eliminate_unit_productions()`

This method removes all unit productions (productions where the RHS is a single nonterminal).

**Algorithm:**

1. Build a **unit-reachability graph**: for each nonterminal $A$, compute the set of nonterminals reachable via unit productions.
2. Use a fixed-point iteration: if $A \rightarrow B$ and $B \rightarrow C$, then $C$ is reachable from $A$.
3. Replace each unit production $A \rightarrow B$ with all non-unit productions of $B$, transitively.

**Example from Variant 21:**

* After epsilon elimination, we have $S \rightarrow A$ (unit production).
* We find all non-unit productions of $A$: $A \rightarrow d$, $A \rightarrow dS$, $A \rightarrow aBdB$.
* We add these to $S$: $S \rightarrow d$, $S \rightarrow dS$, $S \rightarrow aBdB$.
* The unit production $S \rightarrow A$ is then removed.

#### `eliminate_inaccessible_symbols()`

This method removes all nonterminals that are not reachable from the start symbol.

**Algorithm:**

1. Start with the set containing only the start symbol $S$.
2. Iteratively add all nonterminals that appear on the RHS of productions of already-reachable nonterminals.
3. Remove all nonterminals not in the reachable set.

**Example from Variant 21:**

* Starting from $S$, we can reach $A$, $B$, $C$ through the productions.
* The nonterminal $D$ has no incoming edges from the reachable set, so $D$ is inaccessible and is removed.

#### `eliminate_non_productive_symbols()`

This method removes all nonterminals that cannot derive any terminal string.

**Algorithm:**

1. Initialize the set of productive symbols with all terminals.
2. Iteratively add any nonterminal whose productions have all RHS symbols already productive.
3. Remove all nonterminals not in the productive set.
4. If the start symbol becomes non-productive, the grammar is simplified to generate nothing.

**Example from Variant 21:**

* After previous steps, all remaining nonterminals are productive because each can eventually reach a terminal string.

#### `to_chomsky_normal_form()`

This method converts all productions into CNF-compliant forms.

**Algorithm:**

1. **Terminal replacement**: For each production with length $\geq 2$, replace any terminal $a$ in the RHS with a fresh nonterminal $T_a$, and add the production $T_a \rightarrow a$.
2. **Binarization**: For productions with more than 2 symbols, introduce fresh auxiliary nonterminals. For example, $A \rightarrow B C D E$ becomes $A \rightarrow B X_1$, $X_1 \rightarrow C X_2$, $X_2 \rightarrow D E$.

**Example from Variant 21:**

* The production $A \rightarrow aBdB$ is transformed:
  * Replace terminals: $A \rightarrow T_a B T_d B$.
  * Binarize: $A \rightarrow T_a X_1$, $X_1 \rightarrow B X_2$, $X_2 \rightarrow T_d B$.
  * Add terminal productions: $T_a \rightarrow a$, $T_d \rightarrow d$.

#### `is_cnf()`

This validation method checks whether every production satisfies the CNF constraints.

**Validation rules:**

* For each production $A \rightarrow \alpha$:
  * If $|\alpha| = 1$, then $\alpha$ must be a terminal.
  * If $|\alpha| = 2$, then both symbols must be nonterminals.
  * If $|\alpha| \notin \{1, 2\}$, the production violates CNF.
* Returns `True` only if all productions satisfy these rules.


### Execution Pipeline

The `run_pipeline()` function orchestrates all transformations in a strict order:

```python
def run_pipeline(grammar: CFG) -> CFG:
    print(grammar.pretty("Initial Grammar"))
    
    step_1 = grammar.eliminate_epsilon_productions()
    print(step_1.pretty("1) After eliminating epsilon productions"))
    
    step_2 = step_1.eliminate_unit_productions()
    print(step_2.pretty("2) After eliminating unit (renaming) productions"))
    
    step_3 = step_2.eliminate_inaccessible_symbols()
    print(step_3.pretty("3) After eliminating inaccessible symbols"))
    
    step_4 = step_3.eliminate_non_productive_symbols()
    print(step_4.pretty("4) After eliminating non-productive symbols"))
    
    step_5 = step_4.to_chomsky_normal_form()
    print(step_5.pretty("5) Chomsky Normal Form"))
    
    return step_5
```

**Key design decisions:**

1. **Strict sequencing**: Each step depends on the previous ones. For instance, inaccessible elimination must come after epsilon elimination to ensure correctness.
2. **Immutability**: Each method returns a new `CFG` object without modifying the original, enabling easy inspection of intermediate stages.
3. **Detailed output**: Each transformation stage is printed with a title and formatted production list, making the process transparent and verifiable.
4. **Validation**: At the end, the pipeline validates that the final grammar is indeed in CNF.


## Program Output

### Execution Commands

Run with default Variant 21 grammar:

```bash
python3 main.py
```

Run with a custom grammar file:

```bash
python3 main.py --input your_grammar.txt
```

or using the short form:

```bash
python3 main.py -i your_grammar.txt
```

### Observed Output for Variant 21

When executed, the program prints five transformation stages:

**Stage 0: Initial Grammar**

Shows the original grammar with all nonterminals, terminals, and productions as parsed from the file.

**Stage 1: After Epsilon Elimination**

* The explicit production $C \rightarrow \varepsilon$ is removed.
* New productions are generated for all nullable contexts. For example:
  * Original: $B \rightarrow AC$ becomes $B \rightarrow A | C$ (because $C$ is nullable).
  * Original: $S \rightarrow AC$ becomes $S \rightarrow A | AC$ (only $C$ is nullable).

**Stage 2: After Unit Production Elimination**

* Unit productions like $S \rightarrow A$ are replaced with the non-unit productions of $A$.
* The nonterminal set and count remain the same, but productions are redistributed.

**Stage 3: After Inaccessible Symbol Elimination**

* The nonterminal $D$ is removed because it is not reachable from $S$.
* The production $D \rightarrow ab$ is also removed.
* The nonterminal set shrinks from 5 to 4 members: $\{S, A, B, C\}$.

**Stage 4: After Non-Productive Symbol Elimination**

* In this case, all remaining nonterminals are productive, so no further elimination occurs.
* The grammar remains unchanged from the previous stage.

**Stage 5: Chomsky Normal Form**

* Terminal symbols appearing in productions of length $\geq 2$ are replaced with helper nonterminals $T_a$, $T_b$, $T_d$.
* Long productions are binarized using auxiliary nonterminals $X$, $X_1$, $X_2$, etc.
* New helper productions are added: $T_a \rightarrow a$, $T_b \rightarrow b$, $T_d \rightarrow d$.
* Example binarization: $A \rightarrow aBdB$ becomes three productions:
  * $A \rightarrow T_a X_4$
  * $X_4 \rightarrow B X_5$
  * $X_5 \rightarrow T_d B$

**Final Validation**

The program prints `CNF validation: True` if all productions comply with the CNF rules. For Variant 21, this is always true after the transformations.


## Difficulties Faced

### Epsilon Elimination Correctness

**Challenge**: When removing epsilon productions, we must generate all valid combinations of removing nullable symbols from each production's RHS. Failure to generate all combinations would lose part of the language.

**Solution**: Used an iterative bitmask approach: for each production with nullable positions, we generate $2^k$ variants (where $k$ is the number of nullable symbols), systematically including and excluding nullable symbols. This ensures all valid derivations are preserved.

### Unit Production Chains

**Challenge**: Unit productions can form chains like $A \rightarrow B \rightarrow C \rightarrow D$. A naive approach that only processes immediate unit productions would miss transitive reachability.

**Solution**: Built a unit-reachability graph using a fixed-point iteration. For each nonterminal, we compute the transitive closure of all reachable nonterminals via unit productions, then gather all non-unit productions from those reachable symbols.

### Helper Symbol Consistency

**Challenge**: When binarizing long productions and introducing terminal replacements, fresh helper nonterminals must be unique to avoid collisions and overwriting.

**Solution**: Implemented a `_fresh_nonterminal()` method that generates unique names by testing candidates and incrementing a counter. For example, if `X` already exists, it tries `X_1`, `X_2`, etc.

### Flexible Input Parsing

**Challenge**: Users might input grammars in different formats: terminals can be multi-character strings, symbols can be concatenated or space-separated, and epsilon can be represented multiple ways.

**Solution**: Implemented a parser that:
* Recognizes multiple epsilon representations (`ε`, `eps`, `epsilon`, empty string).
* Supports both compact notation (e.g., `aBdB` → `[a, B, d, B]`) and space-separated notation.
* Validates that every symbol in a rule is declared in VN or VT, providing clear error messages for typos.

### Generic Implementation

**Challenge**: The CNF conversion algorithm had to be universal, not hardcoded for Variant 21's specific structure.

**Solution**: Used a data-driven approach where all grammar information is stored in generic sets and dictionaries. The transformation methods operate on these abstract structures and work for any grammar, as demonstrated by the `--input` flag support.


## Conclusions

### Primary Objectives Achieved

1. **CNF Conversion**: The grammar was successfully normalized according to the required five-step transformation pipeline and converted to valid Chomsky Normal Form. The final CNF validation confirmed all productions comply with the canonical forms $A \rightarrow BC$ and $A \rightarrow a$.

2. **Implementation Quality**: The solution is well-structured, reusable, and extensively documented. The `CFG` class can process any context-free grammar, not just Variant 21, fulfilling the bonus objective.

3. **Transparency**: The step-by-step output at each transformation stage makes the process transparent and verifiable. Students and instructors can see exactly how the grammar evolves through each normalization step.

### Technical Insights

* **Grammar Simplification**: Variant 21 demonstrated how inaccessible symbol elimination can significantly reduce grammar complexity (removing nonterminal $D$ and its production).

* **Transformation Order Matters**: The strict sequencing of transformations (epsilon → unit → inaccessible → non-productive → CNF) is essential. For example, unit production elimination depends on epsilon elimination being completed first.

* **Helper Symbol Generation**: The CNF conversion requires systematic introduction of helper nonterminals. This process preserves the original language while enforcing structural constraints.

### Practical Significance

This laboratory provided deep, hands-on experience with:

* Formal grammar analysis and manipulation.
* Understanding why CNF is a crucial intermediate form for parsing algorithms.
* Algorithm design for fixed-point computations (nullable nonterminals, reachability, productivity).
* Writing robust, general-purpose code that works beyond a single example.
