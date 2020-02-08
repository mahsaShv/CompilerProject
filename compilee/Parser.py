import compilee.CompilerScanner as scanner
import csv
import compilee.CodeGenerator as CG

file_name = 'mahsa.txt'
table_name = '1242.csv'
scanner = scanner.Scanner(file_name)
STable = dict()
cg = CG.CodeGenerator(STable)
PT_reader = csv.DictReader(open(table_name, 'r'), delimiter=',')
PT_list = []
IDs = []

for row in PT_reader:
    PT_list.append(row)

state = 0
token = scanner.next_token()
parse_stack = []
id_stack = []
arg_stack = []
type_stack = []
temp_id = None


class Symbol:
    def __init__(self, symbol_type=None):
        self.symbol_type = symbol_type
        self.func_return_type = None
        self.arg_count = None
        self.arg_type_list = None
        self.var_type = None
        self.var_value = None

    def def_func(self, ret_type, arg_count, arg_type_list):
        self.__init__('func')
        if len(arg_type_list) != arg_count:
            print('Function arg error')
            exit()
        self.func_return_type = ret_type
        self.arg_count = arg_count
        self.arg_type_list = arg_type_list
        return self

    def def_var(self, var_type, var_value):
        self.__init__('var')
        self.var_type = var_type
        self.var_value = var_value
        return self

    def def_proc(self, arg_count, arg_type_list):
        self.__init__('func')
        if len(arg_type_list) != arg_count:
            print('Procedure arg error')
            exit()
        self.arg_count = arg_count
        self.arg_type_list = arg_type_list
        return self


def generate_code(func_name, var=None):
    global temp_id, STable, cg

    if func_name == 'NoSem':
        return
    elif func_name == '@push_id':
        if var in STable:
            cg.push(var)
        else:
            print('Variable not declared.')
    elif func_name == "@ADD":
        cg.sum()
    elif func_name == '@def_var':
        temp_id = cg.pop()
    elif func_name == '@set_type':
        STable[temp_id] = var
    elif func_name == '@MUL':
        cg.mult()
    elif func_name == '@DIV':
        cg.div()
    elif func_name == '@MOD':
        cg.mod()

    elif func_name == '@push_new':
        id_stack.append(var)
        STable[var] = []
        cg.push(var)
    elif func_name == '@set_type':
        tok = id_stack.pop()
        STable[tok].append(var)
        cg.set_type(var)
    elif func_name == '@push_new_func':
        STable[var] = Symbol('func')
        id_stack.append(var)
    elif func_name == '@func_left_acc':
        pass
    elif func_name == '@func_right_acc':
        pass
    elif func_name == '@zero_arg':
        STable[id_stack[-1]].def_func(None, 0, [])
    elif func_name == '@push_type':
        type_stack.append(var)
    elif func_name == '@set_func_type':
        symb_id = id_stack.pop()
        STable[symb_id].func_return_type = type_stack.pop()
        cg.function(symb_id)
    elif func_name == '@func_block':
        cg.func_block()

    elif func_name == '@push_inp':
        cg.read_func()

    elif func_name == '@write_str':
        cg.write_str()


while token != 'EOF':
    var = token
    if token not in scanner.tokens:
        token = 'id'
    st = PT_list[state][token].split()
    if st[0] == 'REDUCE':
        state = parse_stack.pop()
        st = PT_list[state][st[1]].split()
        if st[0] == 'GOTO':
            state = int("".join(list(st[1])[1:]))
            generate_code(st[2])
        else:
            print('GOTO ERROR In state: ', state, ' And commands: ', st)

    elif st[0] == 'PUSH_GOTO':
        parse_stack.append(state)
        state = int("".join(list(st[1])[1:]))
        generate_code(st[2], var)

    elif st[0] == 'SHIFT':
        state = int("".join(list(st[1])[1:]))
        generate_code(st[2], var)
        token = scanner.next_token()

    else:
        print('Parser Error! In state: ', state, ' And commands: ', st)
        exit()

print('Compile done!')
cg.print_to_file()
