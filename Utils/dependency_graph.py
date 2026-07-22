#dependency_graph
from graphviz import Digraph

def build_dependency_graph(tac_code):
    dot = Digraph()
    
    for line in tac_code:
        if '=' not in line:
            continue

        left, right = line.split('=', 1)
        left = left.strip()
        right = right.strip()

        parts = right.split()

        # Case 1: simple assignment → a = b
        if len(parts) == 1:
            dot.node(left)
            dot.node(parts[0])
            dot.edge(parts[0], left)

        # Case 2: expression → a = b + c
        elif len(parts) == 3:
            op1, operator, op2 = parts

            op_node = f"{operator}_{id(line)}"

            dot.node(left)
            dot.node(op1)
            dot.node(op2)
            dot.node(op_node, operator)

            dot.edge(op1, op_node)
            dot.edge(op2, op_node)
            dot.edge(op_node, left)

    return dot