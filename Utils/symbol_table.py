#symbol_table.py
class SymbolTable:
    def __init__(self):
        self.table = {}
        self.has_error = False

    def declare(self, name, typ):
        if name in self.table:
            print(f"Semantic Error: {name} already declared")
            self.has_error = True
        else:
            self.table[name] = typ

    def check(self, name):
        if name not in self.table:
            print(f"Semantic Error: {name} not declared")
            self.has_error = True

    def display(self):
        print("\nSymbol Table:")
        for k, v in self.table.items():
            print(k, ":", v)
    
    def remove(self, name):
        if name in self.table:
            del self.table[name]
    
    def declare_function(self, name):
        if name in self.table:
            print(f"Semantic Error: Function {name} already declared")
            self.has_error = True
        else:
            self.table[name] = "function"
    