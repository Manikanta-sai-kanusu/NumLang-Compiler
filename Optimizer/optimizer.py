# optimizer.py

class Optimizer:
    def __init__(self, tac_code):
        self.tac_code = tac_code
        self.constants = {}   # store constant values

    def optimize(self):
        optimized = []

        for line in self.tac_code:
            parts = line.split()

            # -----------------------------
            # Skip control flow lines
            # -----------------------------
            if line.startswith("ifFalse") or line.startswith("goto") or line.endswith(':'):
                optimized.append(line)
                continue

            # -----------------------------
            # Assignment: x = value
            # -----------------------------
            if len(parts) == 3:
                var, _, value = parts

                # ONLY store constant if it's pure number
                if value.isdigit():
                    self.constants[var] = value
                else:
                    #  DO NOT propagate variables blindly
                    if value in self.constants and value.isdigit():
                        value = self.constants[value]

                optimized.append(f"{var} = {value}")

            # -----------------------------
            # Expression: t1 = a + b
            # -----------------------------
            elif len(parts) == 5:
                left, _, op1, operator, op2 = parts

                # ONLY replace if BOTH are constants
                if op1.isdigit() and op2.isdigit():
                    result = eval(f"{op1}{operator}{op2}")
                    optimized.append(f"{left} = {result}")
                    self.constants[left] = str(result)
                else:
                    # ❌ DO NOT replace variables like i
                    optimized.append(line)

            else:
                optimized.append(line)

        return optimized

    def display(self, optimized_code):
        print("\nOptimized Code:")
        for line in optimized_code:
            print(line)