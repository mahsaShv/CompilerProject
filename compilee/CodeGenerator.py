class CodeGenerator:
    def __init__(self):
        self.file = open('mahsa.ll', 'r+')
        self.file.truncate()
        self.temp_num = 1
        self.semantic_stack = []

    def getType(self, a):
        if isinstance(a, int):
            return "i4"
        if isinstance(a, float):
            return "float"
        if isinstance(a, bool):
            return "i1"

    def getTemp(self):
        temp = "%" + str(self.temp_num)
        self.temp_num += 1
        return temp

    def push(self, id):
        self.semantic_stack.append(id)

    def sum(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b)):
            if isinstance(a, int):
                self.file.write(self.getTemp() + " =" + "add " + self.getType(a) + " %a, %b")
            elif isinstance(a, float):
                self.file.write(self.getTemp() + " =" + "fadd " + self.getType(a) + " %a, %b")

        else:
            print("CG Error")

    def mult(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b)):
            if isinstance(a, int):
                self.file.write(self.getTemp() + " =" + "mul " + self.getType(a) + " %a, %b")
            elif isinstance(a, float):
                self.file.write(self.getTemp() + " =" + "fmul " + self.getType(a) + " %a, %b")

    def sub(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b)):
            if isinstance(a, int):
                self.file.write(self.getTemp() + " =" + "sub " + self.getType(a) + " %a, %b")
            elif isinstance(a, float):
                self.file.write(self.getTemp() + " =" + "fsub " + self.getType(a) + " %a, %b")

        else:
            print("CG Error")

    def div(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b)):
            if isinstance(a, int):
                self.file.write(self.getTemp() + " =" + "sdiv " + self.getType(a) + " %a, %b")
            elif isinstance(a, float):
                self.file.write(self.getTemp() + " =" + "fdiv " + self.getType(a) + " %a, %b")

        else:
            print("CG Error")

    def mod(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b)):
            if isinstance(a, int):
                self.file.write(self.getTemp() + " =" + "srem " + self.getType(a) + " %a, %b")
            elif isinstance(a, float):
                self.file.write(self.getTemp() + " =" + "frem " + self.getType(a) + " %a, %b")

        else:
            print("CG Error")

    def bitwiseAnd(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b) and isinstance(a,int)):
            self.file.write(self.getTemp() + " =" + "and " + self.getType(a) + " %a, %b")

        else:
            print("CG Error")

    def bitwiseOr(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b) and isinstance(a, int)):
            self.file.write(self.getTemp() + " =" + "or " + self.getType(a) + " %a, %b")

        else:
            print("CG Error")

    def bitwiseXOr(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b) and isinstance(a, int)):
            self.file.write(self.getTemp() + " =" + "xor " + self.getType(a) + " %a, %b")

        else:
            print("CG Error")

    def logicalAnd(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b) and isinstance(a, int)):
            self.file.write(self.getTemp() + " =" + "xor " + self.getType(a) + " %a, %b")

        else:
            print("CG Error")

    def logicalOr(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b) and isinstance(a, int)):
            self.file.write(self.getTemp() + " =" + "xor " + self.getType(a) + " %a, %b")

        else:
            print("CG Error")

    def minus(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b)):
            if isinstance(a, int):
                self.file.write(self.getTemp() + " =" + "srem " + self.getType(a) + " %a, %b")
            elif isinstance(a, float):
                self.file.write(self.getTemp() + " =" + "frem " + self.getType(a) + " %a, %b")

        else:
            print("CG Error")
