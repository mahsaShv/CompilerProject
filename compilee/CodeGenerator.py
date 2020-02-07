class CodeGenerator:
    def __init__(self):
        self.file = open('mahsa.ll', 'r+')
        self.file.truncate()
        self.temp_num = 1
        self.semantic_stack = []
        self.semantic_table = {}
        self.loop_num = 0
        self.pc = 0
        self.code = {}

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

    def generate_loop_label(self):
        loop_label = '' + str(self.loop_num)
        self.loop_num += 1
        return loop_label

    def push(self, id):
        self.semantic_stack.append(id)

    def pop(self):
        return self.semantic_stack.pop()

    def loop_label(self):
        label = self.generate_loop_label()
        self.semantic_stack.append(label)
        label = ['<label>: ' + label + ': ']
        self.code[self.pc] = label
        self.pc += 1

    def loop_true(self, label):
        expr_ans = self.semantic_stack.pop()
        true_label = self.generate_loop_label()
        false_label = self.generate_loop_label()
        self.code[self.pc] = ['br', 'i1', '%' + expr_ans + ', ', 'label %' + true_label, ', label %' + false_label]
        self.semantic_stack.append(false_label)
        self.code[self.pc + 1] = ['<label>: ' + true_label + ': ']
        self.pc += 2

    def loop_end(self, label):
        false_label = self.semantic_stack.pop()
        self.code[self.pc] = ['br label %' + self.semantic_stack.pop()]
        self.code[self.pc + 1] = ['<label>: ' + false_label + ': ']
        self.pc += 2

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

    def sum(self, a, b):
        if (self.getType(a) == self.getType(b)) or () or ():
            self.file(self.getTemp() + " =" + "add " + self.getType(a) + " %a, %b")
            self.file("add " + self.getType(a) + " %a, %b")

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
        if (self.getType(a) == self.getType(b) and isinstance(a, int)):
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

    # TODO
    def push_new(self, var):
        pass

    # TODO
    # pop id name, set the type for it, wait for further instructions
    def set_type(self, var):
        pass

    def push_new_func(self, var):
        self.semantic_stack.append(var)

    def set_func_type(self, var):
        func_type = ''
        if var == 'integer':
            func_type += 'i32 '
        elif var == 'boolean':
            func_type += 'i1 '
        elif var == 'real':
            func_type += 'float '
        elif var == 'string' or var == 'char':
            func_type += 'i32* '
        self.semantic_stack.append(func_type)

    def func_left_acc(self, var):
        pass

    def assign_var(self, var=None):
        name = self.semantic_stack.pop()
        res_name = self.semantic_stack.pop()
        self.semantic_stack.append(res_name)

    def assign(self, var=None):
        expr_ans = self.semantic_stack.pop()
        assignment_id = self.semantic_stack.pop()
        self.code[self.pc] = ['store', '', ', ']

    def get_type(self, var1, var2):
        pass
