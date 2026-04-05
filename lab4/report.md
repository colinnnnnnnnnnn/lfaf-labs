# Regular Expressions

### Course: Formal Languages & Finite Automata
### Author: Poiata Calin

----

## Theory

Regular expressions are formal descriptions of sets of strings. They are used to describe patterns compactly and are one of the most practical tools in formal language processing, lexical analysis, validation, search, and text generation.

In theory, a regular expression defines a regular language. In practice, the same idea is implemented in many programming languages and tools to match, validate, split, and generate strings that follow a specific structure.

The basic operations used in regular expressions are:

* concatenation, meaning symbols are read one after another;
* alternation, meaning one of several branches can be chosen;
* grouping, meaning a subexpression is treated as a single unit;
* repetition, meaning a symbol or group can appear multiple times;
* optionality, meaning a symbol or group may appear zero or one time.

For this laboratory, the focus is not only on matching regular expressions, but also on interpreting them dynamically and generating valid strings from them.


## Objectives

* Learn what regular expressions are and where they are used.
* Implement a Python program that interprets regular expressions dynamically.
* Generate valid strings for a set of regular expressions without hardcoding the expected outputs.
* Limit unbounded repetition to 5 occurrences so that the generated strings remain short and readable.
* Add a bonus function that prints the sequence of processing steps for a generated string.
* Analyze the behavior of the program for Variant 1.


## Variant 1

The program in `main.py` processes the following regular expressions:

* `(a|b)(c|d)E^+G?`
* `P(Q|R|S)T(UV|W|X)*Z^+`
* `1(0|1)*2(3|4)^5(36)`

These expressions combine grouping, alternation, optional symbols, repetition, and exact repetition.


## Implementation Description

### General Idea

The solution does not hardcode any generation rules for the provided patterns. Instead, it:

* parses the regular expression into an abstract syntax tree, also called AST;
* walks the AST recursively;
* chooses one valid branch for alternations;
* repeats nodes according to the quantifier attached to them;
* concatenates the generated pieces into a final valid string.

This makes the generator reusable for any expression that follows the supported grammar.


### AST Nodes

The implementation uses four node types:

* `Lit` for a literal character;
* `Alt` for alternation between several choices;
* `Group` for grouped sequences;
* `Rep` for repetition nodes.

The `Rep` node stores:

* the repeated node itself;
* the repetition mode;
* a repetition count for exact repetition.


### Parser

The `Parser` class reads the expression character by character and transforms it into an AST.

Supported grammar features:

* literal symbols;
* parenthesized groups;
* alternation using `|`;
* optional repetition using `?`;
* star repetition using `*`;
* plus repetition using `^+`;
* exact repetition using `^n`, where `n` is a digit.

The parser works recursively:

* `parse_seq()` reads a sequence of atoms until it reaches `|`, `)` or the end of the pattern;
* `parse_atom()` handles a literal symbol or a parenthesized subexpression;
* `parse_quantifier()` attaches a repetition rule to the atom if one follows it.

This design keeps the parser small while still supporting the custom syntax used in the laboratory.


### String Generator

The generator is implemented through two functions:

* `gen(nodes, steps=None)` generates a full string from a sequence of AST nodes;
* `_node(node, steps)` generates the string fragment for a single node.

Generation rules:

* a literal emits its character directly;
* a group generates all nodes inside it in order;
* an alternation randomly selects one of the available branches;
* a repetition node expands its child a random number of times, depending on the mode.

The repetition limit is controlled by `MAX_REPEAT = 5`, which is used for `*` and `^+`.

The supported repetition modes are:

* `opt` for zero or one occurrence;
* `star` for zero up to five occurrences;
* `plus` for one up to five occurrences;
* `exact` for the exact number specified after `^`.


### Step-by-Step Processing

The bonus feature is enabled by the `show_steps` parameter in `generate()`.

When this option is active, the program records and prints the sequence of actions taken during generation, such as:

* entering a group;
* choosing a branch of an alternation;
* deciding how many times to repeat a node;
* emitting individual literal characters.

This is useful for explaining how a final string was produced from the expression.


### Multiple Sample Generation

The `generate_many(pattern, n=6)` function creates several distinct strings for the same pattern.

It repeatedly generates new candidates, stores unique results in a set, and stops after collecting the requested number of samples or after enough attempts.

This demonstrates that the same expression can produce different valid words.


## Program Output

The `main.py` file prints the following for each pattern:

* the pattern itself;
* a set of generated samples;
* the processing steps for one generated example;
* the final result of that example.

Because the generator uses randomness, the exact samples and step sequence may differ from run to run.

Example output observed during execution:

```text
Pattern 1: (a|b)(c|d)E^+G?
Samples: {adEEE, acEE, bdEE, bcEG, bdEEEG, bdEEEE}
Steps for one example:
  Pattern: (a|b)(c|d)E^+G?
    1. Alternation — pick branch 2 of 2
    2. Emit 'b'
    3. Alternation — pick branch 2 of 2
    4. Emit 'd'
    5. Repeat (plus) — 5 time(s)
    6. Emit 'E'
    7. Emit 'E'
    8. Emit 'E'
    9. Emit 'E'
    10. Emit 'E'
    11. Repeat (opt) — 1 time(s)
    12. Emit 'G'
Result : bdEEEEEG

Pattern 2: P(Q|R|S)T(UV|W|X)*Z^+
Samples: {PRTWUVZ, PQTUVUVUVUVZZ, PSTXUVXZZZ, PSTUVWUVWUVZZZZ, PQTWXXZZZZZ, PQTWZZZZ}
Steps for one example:
  Pattern: P(Q|R|S)T(UV|W|X)*Z^+
    1. Emit 'P'
    2. Alternation — pick branch 1 of 3
    3. Emit 'Q'
    4. Emit 'T'
    5. Repeat (star) — 0 time(s)
    6. Repeat (plus) — 5 time(s)
    7. Emit 'Z'
    8. Emit 'Z'
    9. Emit 'Z'
    10. Emit 'Z'
    11. Emit 'Z'
Result : PQTZZZZZ

Pattern 3: 1(0|1)*2(3|4)^5(36)
Samples: {123443436, 1123434436, 124434436, 1011124343336, 110023333436, 1123433436}
Steps for one example:
  Pattern: 1(0|1)*2(3|4)^5(36)
    1. Emit '1'
    2. Repeat (star) — 0 time(s)
    3. Emit '2'
    4. Repeat (exact) — 5 time(s)
    5. Alternation — pick branch 1 of 2
    6. Emit '3'
    7. Alternation — pick branch 2 of 2
    8. Emit '4'
    9. Alternation — pick branch 1 of 2
    10. Emit '3'
    11. Alternation — pick branch 1 of 2
    12. Emit '3'
    13. Alternation — pick branch 1 of 2
    14. Emit '3'
    15. Enter group
    16. Emit '3'
    17. Emit '6'
Result : 123433336
```


## Difficulties Faced

Several implementation details required attention:

* The regular expressions are not interpreted by a built-in regex engine; they are parsed manually, so the grammar had to be defined carefully.
* The program uses a custom quantifier syntax with `^+` and `^n`, which is different from standard regular-expression syntax and therefore needed dedicated parsing logic.
* Repetition can produce very long strings if left unrestricted, so a limit of 5 was necessary for `*` and `+`-like behavior.
* Because the output is random, it was important to add step tracing so the generation process can still be explained and verified.
* Some expressions contain nested structures, so the recursive parser and generator had to preserve the correct order of evaluation.


## Conclusions

The laboratory objective was achieved: the program interprets regular expressions dynamically and generates valid strings from them without hardcoding the output for each variant.

Variant 1 was successfully processed, and the implementation demonstrates the main regular-expression operations: concatenation, alternation, grouping, optionality, and repetition.

The bonus tracing feature makes the generation process transparent and easier to study. Limiting unbounded repetition to 5 occurrences keeps the results practical while still showing the behavior of the expressions.

Overall, this laboratory provided a practical understanding of how regular expressions can be parsed and evaluated as formal objects, not only used as matching patterns.