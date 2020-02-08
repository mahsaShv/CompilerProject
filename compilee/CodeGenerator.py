class CodeGenerator:
    def __init__(self, STable):
        self.file = open('mahsa.ll', 'r+')
        self.file.truncate()
        self.temp_num = 1
        self.semantic_stack = []
        self.semantic_table = {}
        self.loop_num = 0
        self.code = {}
        self.code[0] = ['@.i32 = private unnamed_addr constant [3 x i8] c"%d\\00" ']
        self.code[1] = ['@.i64 = private unnamed_addr constant [4 x i8] c"%lu\\00" ']
        self.code[2] = ['@.i8 = private unnamed_addr constant [3 x i8] c"%c\\00" ']
        self.code[3] = ['@.double = private unnamed_addr constant [4 x i8] c"%lf\\00" ']
        self.code[4] = ['@.i1 = private unnamed_addr constant [3 x i8] c"%d\\00" ']
        self.code[5] = ['@.str = private unnamed_addr constant [3 x i8] c"%s\\00" ']
        self.code[6] = ['declare i32 @scanf(i8*, ...)']
        self.code[7] = ['declare i32 @printf(i8*, ...)']

        self.pc = len(self.code)
        self.symbol_table = STable

    def print_to_file(self):
        for row in self.code:
            print(row)

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
                self.file.write(self.getTemp() + " =" + "add " + self.getType(a) + " %" + a + ", " + "%" + b)
            elif isinstance(a, float):
                self.file.write(self.getTemp() + " =" + "fadd " + self.getType(a) + " %" + a + ", " + "%" + b)

        else:
            print("CG Error")

    def mult(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b)):
            if isinstance(a, int):
                self.file.write(self.getTemp() + " =" + "mul " + self.getType(a) + " %" + a + ", " + "%" + b)
            elif isinstance(a, float):
                self.file.write(self.getTemp() + " =" + "fmul " + self.getType(a) + " %" + a + ", " + "%" + b)

    def sub(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b)):
            if isinstance(a, int):
                self.file.write(self.getTemp() + " =" + "sub " + self.getType(a) + " %" + a + ", " + "%" + b)
            elif isinstance(a, float):
                self.file.write(self.getTemp() + " =" + "fsub " + self.getType(a) + " %" + a + ", " + "%" + b)

        else:
            print("CG Error")

    def div(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b)):
            if isinstance(a, int):
                self.file.write(self.getTemp() + " =" + "sdiv " + self.getType(a) + " %" + a + ", " + "%" + b)
            elif isinstance(a, float):
                self.file.write(self.getTemp() + " =" + "fdiv " + self.getType(a) + " %" + a + ", " + "%" + b)

    def mod(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b)):
            if isinstance(a, int):
                self.file.write(self.getTemp() + " =" + "srem " + self.getType(a) + " %" + a + ", " + "%" + b)
            elif isinstance(a, float):
                self.file.write(self.getTemp() + " =" + "frem " + self.getType(a) + " %" + a + ", " + "%" + b)

        else:
            print("CG Error")

    def bitwiseAnd(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b) and isinstance(a, int)):
            self.file.write(self.getTemp() + " =" + "and " + self.getType(a) + " %" + a + ", " + "%" + b)

        else:
            print("CG Error")

    def bitwiseOr(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b) and isinstance(a, int)):
            self.file.write(self.getTemp() + " =" + "or " + self.getType(a) + " %" + a + ", " + "%" + b)

        else:
            print("CG Error")

    def bitwiseXOr(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b) and isinstance(a, int)):
            self.file.write(self.getTemp() + " =" + "xor " + self.getType(a) + " %" + a + ", " + "%" + b)

        else:
            print("CG Error")

    def logicalAnd(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b) and isinstance(a, int)):
            self.file.write(self.getTemp() + " =" + "xor " + self.getType(a) + " %" + a + ", " + "%" + b)

        else:
            print("CG Error")

    def logicalOr(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b) and isinstance(a, int)):
            self.file.write(self.getTemp() + " =" + "xor " + self.getType(a) + " %" + a + ", " + "%" + b)

        else:
            print("CG Error")

    def minus(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b)):
            if isinstance(a, int):
                self.file.write(self.getTemp() + " =" + "srem " + self.getType(a) + " %" + a + ", " + "%" + b)
            elif isinstance(a, float):
                self.file.write(self.getTemp() + " =" + "frem " + self.getType(a) + " %" + a + ", " + "%" + b)

        else:
            print("CG Error")

    def function(self, id):
        i = 0
        self.code[self.pc] = ['define ' + str(self.set_func_type(self.symbol_table[id].func_return_type)), '@' + id,
                              '( ']

        while i < self.symbol_table[id].arg_count - 1:
            self.code[self.pc] += self.set_type(
                self.symbol_table[id].arg_type_list[i]) + " %" + self.semantic_stack.pop() + ", "
            i += 1
        if self.symbol_table[id].arg_count > 0:
            self.code[self.pc] += self.set_type(
                self.symbol_table[id].arg_type_list[i]) + " %" + self.semantic_stack.pop()
        self.code[self.pc] += " ) {"
        self.pc += 1
        self.code[self.pc] = ["entry:"]
        self.pc += 1

    def func_block(self, id=None):
        self.code[self.pc] = ['ret ', self.set_func_type(self.symbol_table[id].func_return_type), ' %',
                              self.semantic_stack.pop(), " }"]

    def procedure(self, id):
        i = 0
        self.code[self.pc] = ['define void @', id, '( ']

        while i < self.symbol_table[id].arg_count - 1:
            self.code[self.pc] += self.set_type(
                self.symbol_table[id].arg_type_list[i]) + " %" + self.semantic_stack.pop() + ", "

            i += 1

        if self.symbol_table[id].arg_count > 0:
            self.code[self.pc] += self.set_type(
                self.symbol_table[id].arg_type_list[i]) + " %" + self.semantic_stack.pop()
        self.code[self.pc] += " ) {"
        self.pc += 1
        self.code[self.pc] = ["entry:"]
        self.pc += 1

    def proc_block(self, id=None):
        self.code[self.pc] = ['ret void', " }"]

    # def in_dcl(self):

    # TODO
    def push_new(self, var):
        pass

    # TODO
    # pop id name, set the type for it, wait for further instructions
    def set_type(self, type):
        if type == "integer":
            return "i32"
        if type == "real":
            return "float"
        if type == "boolean":
            return "i1"
        if type == "boolean":
            return "i1"
        if type == "character":
            return "char"

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

    def read_func(self):
        var_id = self.semantic_stack.pop()
        self.symbol_table[var_id].var_value = None
        temp_var = self.getTemp()
        if self.symbol_table[var_id].var_type == 'integer':
            self.code[self.pc] = [temp_var,
                                  '= call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8] * @.str, i32 0, i32 0), i32* %' + var_id + ')']
        elif self.symbol_table[var_id].var_type == 'character':
            self.code[self.pc] = [temp_var,
                                  '= call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8] * @.str.1, i32 0, i32 0), i8* %' + var_id + ')']
        self.pc += 1

    def write_str(self, var=None):
        var = self.semantic_stack.pop()
        temp = self.getTemp()
        if self.semantic_table[var].var_type == 'integer':
            self.code[self.pc] = ['%' + temp, '= call i32 (i8*, ...) @printf(i8* getelementptr inbounds'
                                              ' ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), ', 'i32 %' + var + ')']
        elif self.semantic_table[var].var_type == 'float':
            self.code[self.pc] = ['%' + temp, '= call i32 (i8*, ...) @printf(i8* getelementptr inbounds'
                                              ' ([3 x i8], [3 x i8]* @.str.2, i32 0, i32 0), ',
                                  'float %' + var + ')']
        elif self.semantic_table[var].var_type == 'string':
            slash_count = 1
            self.code[self.pc] = ['%' + temp, '= call i32 (i8*, ...) @printf(i8* getelementptr inbounds'
                                              ' ([' + str(
                self.semantic_table[var]['string_size'] + slash_count) + ' x i8],'
                                                                         ' [' + str(
                self.semantic_table[var]['string_size'] + slash_count) + ' x i8]* @' + var + ', i32 0, i32 0))']
        self.pc += 1
