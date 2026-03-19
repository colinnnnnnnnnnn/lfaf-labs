from graphviz import Digraph


def draw_automaton(fa, title, filename):
    """Render a finite automaton as a graph using Graphviz."""
    dot = Digraph(comment=title)
    dot.attr(rankdir="LR", label=title, fontsize="16", labelloc="t")

    # Invisible entry point arrow
    dot.node("", shape="none", width="0", height="0")
    dot.edge("", fa.start_state)

    # Draw states
    for state in sorted(fa.states):
        if state in fa.accept_states:
            dot.node(state, shape="doublecircle")
        else:
            dot.node(state, shape="circle")

    # Draw transitions — group by (source, target) to merge labels
    edge_labels = {}
    for (state, symbol), targets in fa.transitions.items():
        for target in targets:
            key = (state, target)
            edge_labels.setdefault(key, []).append(symbol)

    for (src, dst), symbols in sorted(edge_labels.items()):
        label = ", ".join(sorted(symbols))
        dot.edge(src, dst, label=label)

    dot.render(filename, format="png", cleanup=True)
    print(f"Saved {filename}.png")
