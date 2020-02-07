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
        STable[var] = []
        cg.push(var)
    elif func_name == '@set_type':
        cg.set_type(var)


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
