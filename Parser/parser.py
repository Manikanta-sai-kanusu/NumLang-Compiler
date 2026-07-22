# parser.py
from utils.symbol_table import SymbolTable
from intermediate.tac import TACGenerator
from utils.tree_node import Node

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbol_table = SymbolTable()
        self.tac = TACGenerator()
        self.functions = {}
        self.parse_trees = []
        self.parse_tree_root = None

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        token = self.current_token()
        if token and token[0] == token_type:
            self.pos += 1
        else:
            print(f"Syntax Error near {token}")

    # -----------------------------
    # Expression Handling
    # -----------------------------
    def parse_expression(self):
        return self.parse_logical()
    
    def parse_logical(self):
        left = self.parse_comparison()

        while self.current_token() and self.current_token()[1] in ['&&', '||']:
            op = self.current_token()[1]
            self.eat('OPERATOR')

            right = self.parse_comparison()

            parent = Node(op)
            parent.children.append(left)
            parent.children.append(right)

            temp = self.tac.new_temp()
            self.tac.add(f"{temp} = {self.get_val(left)} {op} {self.get_val(right)}")

            left = parent

        return left
    
    def parse_comparison(self):

        left = self.parse_addition()

        while self.current_token() and self.current_token()[1] in [
            '>',
            '<',
            '>=',
            '<=',
            '==',
            '!='
        ]:

            op = self.current_token()[1]

            self.eat('OPERATOR')

            right = self.parse_addition()

            parent = Node(op)

            parent.children.append(left)

            parent.children.append(right)

            temp = self.tac.new_temp()

            self.tac.add(
                f"{temp} = {self.get_val(left)} {op} {self.get_val(right)}"
            )

            # IMPORTANT
            parent.temp = temp

            left = parent

        return left
    
    def parse_addition(self):

        left = self.parse_multiplication()

        while self.current_token() and self.current_token()[1] in ['+', '-']:

            op = self.current_token()[1]

            self.eat('OPERATOR')

            right = self.parse_multiplication()

            parent = Node(op)

            parent.children.append(left)
            parent.children.append(right)

            # TAC
            temp = self.tac.new_temp()

            self.tac.add(
                f"{temp} = {self.get_val(left)} {op} {self.get_val(right)}"
            )

            parent.temp = temp

            left = parent

        return left
    
    def parse_multiplication(self):

        left = self.parse_power()

        while self.current_token() and self.current_token()[1] in ['*', '/', '%']:

            op = self.current_token()[1]

            self.eat('OPERATOR')

            right = self.parse_power()

            parent = Node(op)

            parent.children.append(left)
            parent.children.append(right)

            # TAC
            temp = self.tac.new_temp()

            self.tac.add(
                f"{temp} = {self.get_val(left)} {op} {self.get_val(right)}"
            )

            parent.temp = temp

            left = parent

        return left
    
    def parse_power(self):

        left = self.parse_primary()

        while self.current_token() and self.current_token()[1] in ['^', '**']:

            op = self.current_token()[1]

            self.eat('OPERATOR')

            right = self.parse_primary()

            parent = Node(op)

            parent.children.append(left)
            parent.children.append(right)

            temp = self.tac.new_temp()

            self.tac.add(
                f"{temp} = {self.get_val(left)} {op} {self.get_val(right)}"
            )

            parent.temp = temp

            left = parent

        return left
    
    def parse_primary(self):

        token = self.current_token()

        # ( expression )

        if token and token[1] == '(':

            self.eat('SYMBOL')

            node = self.parse_expression()

            self.eat('SYMBOL')

            return node

        # FUNCTION CALL

        elif token and token[0] == 'ID' and self.peek() and self.peek()[1] == '(':

            return self.parse_function_call()

        # IDENTIFIER

        elif token and token[0] == 'ID':

            self.symbol_table.check(token[1])

            node = Node(token[1])

            self.eat('ID')

            return node

        # NUMBER

        elif token and token[0] == 'NUMBER':

            node = Node(token[1])

            self.eat('NUMBER')

            return node

        # STRING

        elif token and token[0] == 'STRING':

            node = Node(token[1])

            self.eat('STRING')

            return node

        # BOOLEAN

        elif token and token[1] in ['true', 'false']:

            node = Node(token[1])

            self.eat('KEYWORD')

            return node

        else:

            print(f"Syntax Error near {token}")

            return None
    # -----------------------------
    # num a;
    # -----------------------------
    def parse_declaration(self):
        type_token = self.current_token()
        self.eat('KEYWORD')

        var_token = self.current_token()
        self.eat('ID')

        if self.current_token() and self.current_token()[1] == '[':
            self.eat('SYMBOL')
            self.eat('NUMBER')
            self.eat('SYMBOL')
            self.symbol_table.declare(var_token[1], "array")
        else:
            self.symbol_table.declare(var_token[1], type_token[1])

        self.eat('SYMBOL')
    # -----------------------------
    # a = expression;
    # -----------------------------
    def parse_assignment(self):

        var_token = self.current_token()

        self.eat('ID')

        self.symbol_table.check(var_token[1])

        self.eat('OPERATOR')

        # -----------------------------
        # FUNCTION CALL
        # -----------------------------
        if self.current_token() and self.current_token()[0] == 'ID' and self.peek() and self.peek()[1] == '(':

            func_name = self.current_token()[1]

            self.eat('ID')
            self.eat('SYMBOL')  # (

            args = []

            while self.current_token() and self.current_token()[1] != ')':

                arg = self.parse_expression()

                args.append(self.get_val(arg))

                if self.current_token() and self.current_token()[1] == ',':
                    self.eat('SYMBOL')

            self.eat('SYMBOL')  # )

            temp = self.tac.new_temp()

            args_str = ",".join(map(str, args))

            self.tac.add(
                f"{temp} = call {func_name} {args_str}"
            )

            self.tac.add(
                f"{var_token[1]} = {temp}"
            )

            # Parse tree
            root = Node("=")

            root.children.append(Node(var_token[1]))

            call_node = Node(f"call {func_name}")

            for a in args:
                call_node.children.append(Node(str(a)))

            root.children.append(call_node)

        # -----------------------------
        # NORMAL EXPRESSION
        # -----------------------------
        else:

            expr_node = self.parse_expression()

            def to_string(node):

                if not node.children:
                    return str(node.value)

                left = to_string(node.children[0])
                right = to_string(node.children[1])

                return f"{left} {node.value} {right}"

            value = self.get_val(expr_node)

            self.tac.add(
                f"{var_token[1]} = {value}"
            )

            root = Node("=")

            root.children.append(Node(var_token[1]))
            root.children.append(expr_node)

        # save latest parse tree
        self.parse_tree_root = root

        self.eat('SYMBOL')
    # -----------------------------
    # show a;
    # -----------------------------
    def parse_print(self):
        self.eat('KEYWORD')
        node = self.parse_expression()

        def to_string(n):
            if not n.children:
                return n.value
            return f"{to_string(n.children[0])} {n.value} {to_string(n.children[1])}"

        val = self.get_val(node)
        self.tac.add(f"print {val}")

        self.eat('SYMBOL')

    def parse_if(self):
        self.eat('KEYWORD')
        self.eat('SYMBOL')

        condition = self.parse_expression()

        self.eat('SYMBOL')

        label1 = f"L{self.tac.new_temp()}"
        cond_temp = self.get_val(condition)
        self.tac.add(f"ifFalse {cond_temp} goto {label1}")
        self.eat('SYMBOL')

        while self.current_token() and self.current_token()[1] != '}':
            self.parse_block()

        self.eat('SYMBOL')

        if self.current_token() and self.current_token()[1] == 'else':
            label2 = f"L{self.tac.new_temp()}"
            self.tac.add(f"goto {label2}")
            self.tac.add(f"{label1}:")

            self.eat('KEYWORD')
            self.eat('SYMBOL')

            self.parse_block()

            self.eat('SYMBOL')
            self.tac.add(f"{label2}:")
        else:
            self.tac.add(f"{label1}:")

    # -----------------------------
    # Main Parse Loop
    # -----------------------------
    def parse(self):
        while self.current_token():
            token = self.current_token()

            if token[1] in ['num', 'text', 'bool']:
                self.parse_declaration()

            elif token[0] == 'ID':
                self.parse_assignment()

            elif token[1] == 'show':
                self.parse_print()

            elif token[1] == 'cond':
                self.parse_if()

            elif token[1] == 'loop':
                self.parse_loop()

            elif token[1] == 'func':
                self.parse_function()

            elif token[1] == 'break':
                self.eat('KEYWORD')
                self.tac.add("break")
                self.eat('SYMBOL')
            
            elif token[1] == 'return':
                self.parse_return()

            else:
                print(f"Unexpected token {token}")
                self.pos += 1
    
    def parse_loop(self):
        start = f"L{self.tac.new_temp()}"
        end = f"L{self.tac.new_temp()}"

        self.tac.add(f"{start}:")

        self.eat('KEYWORD')
        self.eat('SYMBOL')

        condition = self.parse_expression()

        self.eat('SYMBOL')

        cond_temp = self.get_val(condition)
        self.tac.add(f"ifFalse {cond_temp} goto {end}")

        self.eat('SYMBOL')

        while self.current_token() and self.current_token()[1] != '}':
            self.parse_block()

        self.eat('SYMBOL')

        self.tac.add(f"goto {start}")
        self.tac.add(f"{end}:")
    
    def parse_function(self):

        self.eat('KEYWORD')  # func

        func_name = self.current_token()[1]

        self.eat('ID')

        self.eat('SYMBOL')  # (

        params = []

        # -----------------------------
        # PARAMETERS
        # -----------------------------
        while self.current_token() and self.current_token()[1] != ')':

            self.eat('KEYWORD')  # type

            param_name = self.current_token()[1]

            params.append(param_name)

            # declare parameter
            self.symbol_table.declare(param_name, "num")

            self.eat('ID')

            if self.current_token() and self.current_token()[1] == ',':
                self.eat('SYMBOL')

        self.eat('SYMBOL')  # )

        self.eat('SYMBOL')  # {

        # -----------------------------
        # START FUNCTION TAC
        # -----------------------------
        func_code_start = len(self.tac.code)

        # -----------------------------
        # FUNCTION BODY
        # -----------------------------
        while self.current_token() and self.current_token()[1] != '}':

            token = self.current_token()

            if token[1] in ['num', 'text', 'bool']:
                self.parse_declaration()

            elif token[0] == 'ID':
                self.parse_assignment()

            elif token[1] == 'show':
                self.parse_print()

            elif token[1] == 'cond':
                self.parse_if()

            elif token[1] == 'loop':
                self.parse_loop()

            elif token[1] == 'return':
                self.parse_return()

            else:
                print(f"Unexpected token in function: {token}")
                self.pos += 1

        self.eat('SYMBOL')  # }

        # -----------------------------
        # CAPTURE FUNCTION TAC
        # -----------------------------
        func_code = self.tac.code[func_code_start:]

        func_code.append("end func")

        self.functions[func_name] = {
            "params": params,
            "code": func_code
        }

        # -----------------------------
        # ADD TO TAC
        # -----------------------------
        self.tac.add(f"func {func_name}")

        for line in func_code:
            self.tac.add(line)

    def parse_for(self):
        self.eat('KEYWORD')  # for
        self.eat('SYMBOL')

        self.parse_assignment()
        condition = self.parse_expression()
        self.eat('SYMBOL')
        self.parse_assignment()

        self.eat('SYMBOL')

        while self.current_token()[1] != '}':
            self.parse_block()

        self.eat('SYMBOL')

    def parse_break(self):
        self.eat('KEYWORD')
        self.tac.add("break")
        self.eat('SYMBOL')
    
    def parse_block(self):

        token = self.current_token()

        if not token:
            return

        if token[1] in ['num', 'text', 'bool']:
            self.parse_declaration()

        elif token[0] == 'ID':
            self.parse_assignment()

        elif token[1] == 'show':
            self.parse_print()

        elif token[1] == 'cond':
            self.parse_if()

        elif token[1] == 'loop':
            self.parse_loop()

        elif token[1] == 'func':
            self.parse_function()

        elif token[1] == 'break':
            self.eat('KEYWORD')
            self.tac.add("break")
            self.eat('SYMBOL')

        elif token[1] == 'return':
            self.parse_return()

        else:
            print(f"Unexpected token {token}")
            self.pos += 1
    
    def parse_return(self):
        self.eat('KEYWORD')  # return
        value = self.parse_expression()
        self.tac.add(f"return {self.get_val(value)}")
        self.eat('SYMBOL')

    def parse_function_call(self):

        func_name = self.current_token()[1]

        self.eat('ID')

        self.eat('SYMBOL')  # (

        args = []

        while self.current_token() and self.current_token()[1] != ')':

            arg = self.parse_expression()

            args.append(self.get_val(arg))

            if self.current_token() and self.current_token()[1] == ',':
                self.eat('SYMBOL')

        self.eat('SYMBOL')  # )

        temp = self.tac.new_temp()

        args_str = ",".join(map(str, args))

        self.tac.add(f"{temp} = call {func_name} {args_str}")

        return Node(temp)

    def peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None
    
    def get_val(self, node):
        if hasattr(node, "temp"):
            return node.temp

        if isinstance(node, Node):
            return node.value

        return node