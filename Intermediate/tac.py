# tac.py

class TACGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 1

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def add(self, instruction):
        self.code.append(instruction)

    def display(self):
        print("\nThree Address Code (TAC):")
        for line in self.code:
            print(line)
            