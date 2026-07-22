#cfg.py
from graphviz import Digraph

def build_cfg(tac_code):
    dot = Digraph()
    
    # Step 1: Create nodes
    for i, line in enumerate(tac_code):
        node_name = f"N{i}"
        dot.node(node_name, line)

    # Step 2: Map labels to indices
    label_map = {}
    for i, line in enumerate(tac_code):
        if line.endswith(':'):
            label = line[:-1]
            label_map[label] = i

    # Step 3: Add edges
    for i, line in enumerate(tac_code):
        current = f"N{i}"

        # -----------------------------
        # IF FALSE (conditional jump)
        # -----------------------------
        if line.startswith("ifFalse"):
            parts = line.split()
            label = parts[-1]

            # False branch
            if label in label_map:
                dot.edge(current, f"N{label_map[label]}", label="False")

            # True branch → next instruction
            if i + 1 < len(tac_code):
                dot.edge(current, f"N{i+1}", label="True")

        # -----------------------------
        # GOTO (unconditional jump)
        # -----------------------------
        elif line.startswith("goto"):
            label = line.split()[1]

            if label in label_map:
                dot.edge(current, f"N{label_map[label]}")

        # -----------------------------
        # NORMAL FLOW
        # -----------------------------
        else:
            if i + 1 < len(tac_code):
                dot.edge(current, f"N{i+1}")

    return dot