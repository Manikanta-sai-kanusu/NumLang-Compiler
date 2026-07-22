#tree_visualizer.py
from graphviz import Digraph

def visualize_tree(root):
    dot = Digraph()

    def add_nodes(node, parent_id=None):
        if node is None:
            return

        node_id = str(id(node))
        label = str(node.value) if hasattr(node, "value") else str(node)
        dot.node(node_id, label)

        if parent_id:
            dot.edge(parent_id, node_id)

        children = node.children if hasattr(node, "children") else []
        for child in children:
            add_nodes(child, node_id)

    add_nodes(root)
    return dot