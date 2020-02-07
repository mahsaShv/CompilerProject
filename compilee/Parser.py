import compilee.CompilerScanner as scanner
import csv
import compilee.CodeGenerator as CG

file_name = 'mahsa.txt'
table_name = '232.csv'
scanner = scanner.Scanner(file_name)
cg = CG.CodeGenerator()
PT_reader = csv.DictReader(open(table_name, 'r'), delimiter=',')
PT_list = []
IDs = []

for row in PT_reader:
    PT_list.append(row)

state = 0
token = scanner.next_token()
parse_stack = []
id_stack = []
STable = dict()
temp_id = None


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
    elif func_name == '@push_new':
        id_stack.append(var)
        STable[var] = []
        cg.push(var)
    elif func_name == '@set_type':
        tok = id_stack.pop()
        STable[tok].append(var)
        cg.set_type(var)
    elif func_name == '@push_new_func':
        pass
    elif func_name == '@set_func_type':
        pass
    elif func_name == '@func_left_acc':
        pass
    elif func_name == '@func_right_acc':
        pass


while token != 'EOF':
    var = token
    if token not in scanner.tokens:
        token = 'id'
    st = PT_list[state][token].split()
    print(st, token, var)
    if st[0] == 'REDUCE':
        state = parse_stack.pop()
        goto_state = PT_list[state][st[1]].split()
        if goto_state[0] == 'GOTO':
            state = goto_state[1][1:]
            generate_code(goto_state[2])
        else:
            print('GOTO ERROR')

    elif st[0] == 'PUSH_GOTO':
        parse_stack.append(state)
        state = int("".join(list(st[1])[1:]))
        generate_code(st[2], var)

    elif st[0] == 'SHIFT':
        state = int("".join(list(st[1])[1:]))
        generate_code(st[2], var)
        token = scanner.next_token()

    else:
        print('Parser Error!')
        print(state)
        exit()

print('Compile done!')


class Symbol:
    def __init__(self, symbol_type):
        self.symbol_type = symbol_type
        self.func_return_type = None
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
