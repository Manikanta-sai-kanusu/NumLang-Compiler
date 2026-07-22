#main.py
from lexer.lexer import tokenize
from parser.parser import Parser
from optimizer.optimizer import Optimizer
from utils.tree_visualizer import visualize_tree
from utils.dependency_graph import build_dependency_graph
from utils.cfg import build_cfg


# MOVE execution logic into a function
def execute_code(optimized_code, functions):

    import re

    memory = {}
    labels = {}
    call_stack = []

    # -----------------------------
    # MAP LABELS
    # -----------------------------
    for i, line in enumerate(optimized_code):
        if line.endswith(':'):
            labels[line[:-1].strip()] = i

    

    # -----------------------------
    # SAFE EXPRESSION EVALUATION
    # -----------------------------
    def eval_expr(expr, mem):

        def replacer(match):

            var = match.group(0)

            if var in mem:
                return str(mem[var])

            return var

        expr = re.sub(
            r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
            replacer,
            expr
        )

        try:
            return eval(expr, {"__builtins__": None}, {})
        except Exception:
            return None

    # -----------------------------
    # EXECUTION LOOP
    # -----------------------------
    pc = 0

    output = []

    steps = 0
    MAX_STEPS = 5000

    while pc < len(optimized_code):

        steps += 1

        if steps > MAX_STEPS:
            output.append("Runtime Error: Infinite Loop")
            break

        line = optimized_code[pc].strip()

        # -----------------------------
        # LABEL
        # -----------------------------
        if line.endswith(':'):
            pc += 1
            continue

        # -----------------------------
        # SKIP FUNCTION DEFINITIONS
        # -----------------------------
        if line.startswith("func"):

            while not optimized_code[pc].startswith("end func"):
                pc += 1

            pc += 1
            continue

        # -----------------------------
        # PRINT
        # -----------------------------
        if line.startswith("print"):

            val = line.split(" ", 1)[1].strip()

            try:
                result = eval_expr(val, memory)
                output.append(str(result))

            except:

                if val.startswith('"') and val.endswith('"'):
                    output.append(val.strip('"'))

                else:
                    output.append(val)

        # -----------------------------
        # CONDITIONAL JUMP
        # -----------------------------
        elif line.startswith("ifFalse"):

            parts = line.split()

            cond = parts[1]
            label = parts[-1]

            cond_val = memory.get(cond, False)

            if not cond_val:
                pc = labels[label]
                continue

        # -----------------------------
        # GOTO
        # -----------------------------
        elif line.startswith("goto"):

            label = line.split()[1]

            pc = labels[label]
            continue

        # -----------------------------
        # FUNCTION CALL
        # -----------------------------
        elif "= call" in line:

            # t1 = call add 5,3

            left, right = line.split("=", 1)

            result_var = left.strip()

            right = right.strip()

            parts = right.split()

            func_name = parts[1]

            arg_string = " ".join(parts[2:]).strip()

            args = []

            if arg_string.strip():

                raw_args = arg_string.split(",")

                for a in raw_args:
                    args.append(eval_expr(a.strip(), memory))

            if func_name not in functions:

                output.append(f"Runtime Error: Function {func_name} not found")
                break

            local_memory = {}

            params = functions[func_name]["params"]

            for idx, param in enumerate(params):

                if idx < len(args):
                    local_memory[param] = args[idx]

            return_value = None

            for stmt in functions[func_name]["code"]:

                stmt = stmt.strip()

                # RETURN
                if stmt.startswith("return"):

                    expr = stmt.split(" ", 1)[1]

                    return_value = eval_expr(expr, local_memory)

                    break

                # ASSIGNMENT
                # -----------------------------
                # FUNCTION CALL
                # -----------------------------
                elif "= call" in line:

                    left, right = line.split("=", 1)

                    result_var = left.strip()

                    right = right.strip()

                    parts = right.split()

                    func_name = parts[1]

                    arg_string = " ".join(parts[2:]).strip()

                    args = []

                    if arg_string:

                        raw_args = arg_string.split(",")

                        for a in raw_args:
                            args.append(eval_expr(a.strip(), memory))

                    # function exists?
                    if func_name not in functions:

                        output.append(f"Runtime Error: Function {func_name} not found")
                        break

                    func_data = functions[func_name]

                    local_memory = {}

                    # map params
                    for idx, param in enumerate(func_data["params"]):

                        if idx < len(args):
                            local_memory[param] = args[idx]

                    return_value = None

                    # execute function body
                    for stmt in func_data["code"]:

                        stmt = stmt.strip()

                        # skip empty
                        if not stmt:
                            continue

                        # skip end func
                        if stmt == "end func":
                            continue

                        # return
                        if stmt.startswith("return"):

                            expr = stmt.split(" ", 1)[1]

                            return_value = eval_expr(expr, local_memory)

                            break

                        # assignment
                        elif "=" in stmt and "call" not in stmt:

                            v, expr = stmt.split("=", 1)

                            v = v.strip()
                            expr = expr.strip()

                            local_memory[v] = eval_expr(expr, local_memory)

                    memory[result_var] = return_value

                    memory[result_var] = return_value

        # -----------------------------
        # NORMAL ASSIGNMENT
        # -----------------------------
        elif "=" in line:

            var, expr = line.split("=", 1)

            var = var.strip()

            expr = expr.strip()

            try:

                memory[var] = eval_expr(expr, memory)

            except Exception as e:

                print("Execution Error:", e)

                memory[var] = None

        pc += 1

    return output
# MAIN PIPELINE FUNCTION
def run_compiler(code):

    # -----------------------------
    # LEXER
    # -----------------------------
    tokens = tokenize(code)

    # -----------------------------
    # PARSER
    # -----------------------------
    parser = Parser(tokens)
    parser.parse()


    tree_graph = None
    if parser.parse_tree_root is not None:
        tree_graph = visualize_tree(parser.parse_tree_root)
        print("TREE GRAPH:", tree_graph)
    
    if parser.symbol_table.has_error:
        return {
            "error": "Semantic Error",
            "tokens": tokens
        }

    symbol_table = parser.symbol_table.table

    # -----------------------------
    # TAC
    # -----------------------------
    tac_code = parser.tac.code

    # -----------------------------
    # OPTIMIZER
    # -----------------------------
    optimizer = Optimizer(tac_code)
    optimized_code = optimizer.optimize()

    # -----------------------------
    # DEPENDENCY GRAPH
    # -----------------------------
    dependency_graph = build_dependency_graph(optimized_code)

    # -----------------------------
    # CFG (Control Flow Graph)
    # -----------------------------
    cfg_graph = build_cfg(optimized_code)

    # -----------------------------
    # EXECUTION
    # -----------------------------
    print("FUNCTIONS:", parser.functions)
    output = execute_code(
        tac_code,
        parser.functions
    )

    return {
        "tokens": tokens,
        "symbol_table": symbol_table,
        "tac": tac_code,
        "optimized": optimized_code,
        "output": output,
        "parse_tree_graph": tree_graph,
        "dependency_graph": dependency_graph,
        "cfg_graph": cfg_graph
    }