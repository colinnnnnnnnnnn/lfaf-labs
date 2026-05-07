from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable


EPSILON_TOKENS = {"", "ε", "eps", "epsilon"}


@dataclass
class CFG:
    nonterminals: set[str]
    terminals: set[str]
    start_symbol: str
    productions: dict[str, set[tuple[str, ...]]]

    def copy(self) -> "CFG":
        return CFG(
            nonterminals=set(self.nonterminals),
            terminals=set(self.terminals),
            start_symbol=self.start_symbol,
            productions={k: set(v) for k, v in self.productions.items()},
        )

    @staticmethod
    def from_rules(
        nonterminals: Iterable[str],
        terminals: Iterable[str],
        start_symbol: str,
        rules: Iterable[str],
    ) -> "CFG":
        nts = set(nonterminals)
        ts = set(terminals)
        if start_symbol not in nts:
            raise ValueError("Start symbol must be in nonterminals")

        productions: dict[str, set[tuple[str, ...]]] = {nt: set() for nt in nts}

        for rule in rules:
            if "->" not in rule:
                raise ValueError(f"Invalid rule format: {rule}")
            lhs, rhs_part = rule.split("->", maxsplit=1)
            lhs = lhs.strip()
            if lhs not in nts:
                raise ValueError(f"Unknown nonterminal on LHS: {lhs}")

            alternatives = [alt.strip() for alt in rhs_part.split("|")]
            for alt in alternatives:
                if alt in EPSILON_TOKENS:
                    rhs: tuple[str, ...] = ()
                else:
                    symbols = alt.split()
                    if len(symbols) == 1 and symbols[0] and " " not in alt:
                        # Support compact notation like dB or aBdB.
                        symbols = list(alt)
                    rhs = tuple(symbols)

                for symbol in rhs:
                    if symbol not in nts and symbol not in ts:
                        raise ValueError(
                            f"Unknown symbol '{symbol}' in rule '{rule}'. "
                            "Every symbol must be declared as terminal or nonterminal."
                        )
                productions[lhs].add(rhs)

        return CFG(nts, ts, start_symbol, productions)

    def _fresh_nonterminal(self, prefix: str) -> str:
        index = 1
        candidate = prefix
        while candidate in self.nonterminals or candidate in self.terminals:
            candidate = f"{prefix}_{index}"
            index += 1
        return candidate

    def eliminate_epsilon_productions(self) -> "CFG":
        new_grammar = self.copy()

        nullable: set[str] = set()
        changed = True
        while changed:
            changed = False
            for lhs, rhs_set in new_grammar.productions.items():
                if lhs in nullable:
                    continue
                for rhs in rhs_set:
                    if len(rhs) == 0 or all(symbol in nullable for symbol in rhs):
                        nullable.add(lhs)
                        changed = True
                        break

        new_productions: dict[str, set[tuple[str, ...]]] = {
            nt: set() for nt in new_grammar.nonterminals
        }

        for lhs, rhs_set in new_grammar.productions.items():
            for rhs in rhs_set:
                if len(rhs) == 0:
                    continue

                nullable_positions = [
                    idx for idx, symbol in enumerate(rhs) if symbol in nullable
                ]

                for mask in product([0, 1], repeat=len(nullable_positions)):
                    to_remove = {
                        nullable_positions[i]
                        for i, bit in enumerate(mask)
                        if bit == 1
                    }
                    candidate = tuple(
                        symbol
                        for idx, symbol in enumerate(rhs)
                        if idx not in to_remove
                    )

                    if len(candidate) == 0:
                        # Classical CNF simplification: remove epsilon productions.
                        continue
                    new_productions[lhs].add(candidate)

        new_grammar.productions = new_productions
        return new_grammar

    def eliminate_unit_productions(self) -> "CFG":
        new_grammar = self.copy()

        unit_graph: dict[str, set[str]] = {nt: {nt} for nt in new_grammar.nonterminals}

        for nt in new_grammar.nonterminals:
            changed = True
            while changed:
                changed = False
                current_targets = list(unit_graph[nt])
                for target in current_targets:
                    for rhs in new_grammar.productions.get(target, set()):
                        if len(rhs) == 1 and rhs[0] in new_grammar.nonterminals:
                            next_nt = rhs[0]
                            if next_nt not in unit_graph[nt]:
                                unit_graph[nt].add(next_nt)
                                changed = True

        rebuilt: dict[str, set[tuple[str, ...]]] = {nt: set() for nt in new_grammar.nonterminals}

        for lhs in new_grammar.nonterminals:
            for reachable in unit_graph[lhs]:
                for rhs in new_grammar.productions.get(reachable, set()):
                    if len(rhs) == 1 and rhs[0] in new_grammar.nonterminals:
                        continue
                    rebuilt[lhs].add(rhs)

        new_grammar.productions = rebuilt
        return new_grammar

    def eliminate_non_productive_symbols(self) -> "CFG":
        new_grammar = self.copy()

        productive: set[str] = set()
        changed = True
        while changed:
            changed = False
            for lhs, rhs_set in new_grammar.productions.items():
                if lhs in productive:
                    continue
                for rhs in rhs_set:
                    if all(
                        symbol in new_grammar.terminals or symbol in productive
                        for symbol in rhs
                    ):
                        productive.add(lhs)
                        changed = True
                        break

        if new_grammar.start_symbol not in productive:
            new_grammar.nonterminals = {new_grammar.start_symbol}
            new_grammar.productions = {new_grammar.start_symbol: set()}
            return new_grammar

        new_grammar.nonterminals = {nt for nt in new_grammar.nonterminals if nt in productive}

        filtered: dict[str, set[tuple[str, ...]]] = {
            nt: set() for nt in new_grammar.nonterminals
        }
        for lhs, rhs_set in new_grammar.productions.items():
            if lhs not in new_grammar.nonterminals:
                continue
            for rhs in rhs_set:
                if all(
                    symbol in new_grammar.terminals or symbol in new_grammar.nonterminals
                    for symbol in rhs
                ):
                    filtered[lhs].add(rhs)

        new_grammar.productions = filtered
        return new_grammar

    def eliminate_inaccessible_symbols(self) -> "CFG":
        new_grammar = self.copy()

        reachable: set[str] = {new_grammar.start_symbol}
        changed = True
        while changed:
            changed = False
            current = set(reachable)
            for nt in current:
                for rhs in new_grammar.productions.get(nt, set()):
                    for symbol in rhs:
                        if symbol in new_grammar.nonterminals and symbol not in reachable:
                            reachable.add(symbol)
                            changed = True

        new_grammar.nonterminals = reachable
        new_grammar.productions = {
            nt: set(new_grammar.productions.get(nt, set())) for nt in reachable
        }
        return new_grammar

    def to_chomsky_normal_form(self) -> "CFG":
        new_grammar = self.copy()

        terminal_alias: dict[str, str] = {}
        cnf_productions: dict[str, set[tuple[str, ...]]] = {
            nt: set() for nt in new_grammar.nonterminals
        }

        def terminal_to_nonterminal(terminal: str) -> str:
            if terminal in terminal_alias:
                return terminal_alias[terminal]
            fresh = new_grammar._fresh_nonterminal(f"T_{terminal}")
            new_grammar.nonterminals.add(fresh)
            cnf_productions.setdefault(fresh, set()).add((terminal,))
            terminal_alias[terminal] = fresh
            return fresh

        for lhs, rhs_set in new_grammar.productions.items():
            for rhs in rhs_set:
                if len(rhs) == 1 and rhs[0] in new_grammar.terminals:
                    cnf_productions[lhs].add(rhs)
                    continue

                transformed = list(rhs)
                if len(transformed) >= 2:
                    for idx, symbol in enumerate(transformed):
                        if symbol in new_grammar.terminals:
                            transformed[idx] = terminal_to_nonterminal(symbol)

                if len(transformed) <= 2:
                    cnf_productions[lhs].add(tuple(transformed))
                else:
                    current_lhs = lhs
                    remaining = transformed
                    while len(remaining) > 2:
                        first_symbol = remaining[0]
                        fresh = new_grammar._fresh_nonterminal("X")
                        new_grammar.nonterminals.add(fresh)
                        cnf_productions.setdefault(fresh, set())
                        cnf_productions[current_lhs].add((first_symbol, fresh))
                        current_lhs = fresh
                        remaining = remaining[1:]
                    cnf_productions[current_lhs].add(tuple(remaining))

        for nt in new_grammar.nonterminals:
            cnf_productions.setdefault(nt, set())

        new_grammar.productions = cnf_productions
        return new_grammar

    def is_cnf(self) -> bool:
        for lhs, rhs_set in self.productions.items():
            if lhs not in self.nonterminals:
                return False
            for rhs in rhs_set:
                if len(rhs) == 1:
                    if rhs[0] not in self.terminals:
                        return False
                elif len(rhs) == 2:
                    if rhs[0] not in self.nonterminals or rhs[1] not in self.nonterminals:
                        return False
                else:
                    return False
        return True

    def formatted_productions(self) -> list[str]:
        lines: list[str] = []
        for lhs in sorted(self.productions):
            rhs_list = sorted(self.productions[lhs])
            if not rhs_list:
                lines.append(f"{lhs} -> <none>")
                continue
            rendered_alts = []
            for rhs in rhs_list:
                rendered_alts.append(" ".join(rhs) if rhs else "ε")
            lines.append(f"{lhs} -> {' | '.join(rendered_alts)}")
        return lines

    def pretty(self, title: str | None = None) -> str:
        header = []
        if title:
            header.append(title)
        header.append(f"VN = {{{', '.join(sorted(self.nonterminals))}}}")
        header.append(f"VT = {{{', '.join(sorted(self.terminals))}}}")
        header.append("P:")
        header.extend(f"  {line}" for line in self.formatted_productions())
        return "\n".join(header)
