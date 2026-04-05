import random

MAX_REPEAT = 5

# --- AST Nodes ---

class Lit:
    def __init__(self, ch): self.ch = ch

class Alt:
    def __init__(self, choices): self.choices = choices

class Group:
    def __init__(self, seq): self.seq = seq

class Rep:
    def __init__(self, node, mode, count=0):
        self.node = node
        self.mode = mode   # 'star' | 'plus' | 'opt' | 'exact'
        self.count = count

# --- Parser ---

class Parser:
    def __init__(self, pattern):
        self.p = pattern
        self.i = 0

    def peek(self): return self.p[self.i] if self.i < len(self.p) else None
    def consume(self): ch = self.p[self.i]; self.i += 1; return ch

    def parse(self):
        nodes = self.parse_seq()
        if self.i != len(self.p):
            raise SyntaxError(f"Unexpected '{self.peek()}' at pos {self.i}")
        return nodes

    def parse_seq(self):
        nodes = []
        while self.peek() not in (None, '|', ')'):
            atom = self.parse_atom()
            q = self.parse_quantifier()
            nodes.append(Rep(atom, **q) if q else atom)
        return nodes

    def parse_atom(self):
        if self.peek() == '(':
            self.consume()
            choices = [self.parse_seq()]
            while self.peek() == '|':
                self.consume()
                choices.append(self.parse_seq())
            self.consume()  # ')'
            return Alt(choices) if len(choices) > 1 else Group(choices[0])
        return Lit(self.consume())

    def parse_quantifier(self):
        ch = self.peek()
        if ch == '*':  self.consume(); return {'mode': 'star'}
        if ch == '?':  self.consume(); return {'mode': 'opt'}
        if ch == '^':
            self.consume()
            if self.peek() == '+': self.consume(); return {'mode': 'plus'}
            if self.peek() and self.peek().isdigit(): return {'mode': 'exact', 'count': int(self.consume())}
        return None

# --- Generator ---

def gen(nodes, steps=None):
    return ''.join(_node(n, steps) for n in nodes)

def _node(node, steps):
    if isinstance(node, Lit):
        if steps is not None: steps.append(f"Emit '{node.ch}'")
        return node.ch

    if isinstance(node, Group):
        if steps is not None: steps.append("Enter group")
        return gen(node.seq, steps)

    if isinstance(node, Alt):
        idx = random.randrange(len(node.choices))
        if steps is not None: steps.append(f"Alternation — pick branch {idx + 1} of {len(node.choices)}")
        return gen(node.choices[idx], steps)

    if isinstance(node, Rep):
        if   node.mode == 'opt':   t = random.randint(0, 1)
        elif node.mode == 'star':  t = random.randint(0, MAX_REPEAT)
        elif node.mode == 'plus':  t = random.randint(1, MAX_REPEAT)
        elif node.mode == 'exact': t = node.count
        if steps is not None: steps.append(f"Repeat ({node.mode}) — {t} time(s)")
        return ''.join(_node(node.node, steps) for _ in range(t))

def generate(pattern, show_steps=False):
    ast = Parser(pattern).parse()
    steps = [] if show_steps else None
    result = gen(ast, steps)
    if show_steps:
        print(f"  Pattern: {pattern}")
        for i, s in enumerate(steps, 1):
            print(f"    {i}. {s}")
        print(f"  Result : {result}")
    return result

def generate_many(pattern, n=6):
    seen, out = set(), []
    for _ in range(n * 50):
        if len(out) >= n: break
        s = generate(pattern)
        if s not in seen:
            seen.add(s); out.append(s)
    return out

# --- Main ---

patterns = [
    ("(a|b)(c|d)E^+G?",       "Pattern 1"),
    ("P(Q|R|S)T(UV|W|X)*Z^+", "Pattern 2"),
    ("1(0|1)*2(3|4)^5(36)",   "Pattern 3"),
]

for pattern, label in patterns:
    print(f"\n{label}: {pattern}")
    print("  Samples:", "{" + ", ".join(generate_many(pattern)) + "}")
    print("  Steps for one example:")
    generate(pattern, show_steps=True)