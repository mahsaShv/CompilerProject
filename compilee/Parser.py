import compilee.CompilerScanner as scanner
import csv
import compilee.CodeGenerator as CG

file_name = 'mahsa.txt'
table_name = 'Table_5.csv'
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
STable_reverse = dict()
in_DCL = True
temp_id = None


def generate_code(func_name, var=None):
    global temp_id, in_DCL, STable, STable_reverse, cg

    if func_name == 'NoSem':
        return
    elif func_name == '@push':
        cg.push(var)
    elif func_name == "@ADD":
        cg.sum()
    elif func_name == '@in_DCL':
        in_DCL = True
    elif func_name == '@def_var':
        temp_id = cg.pop()
    elif func_name == '@set_type':
        STable[temp_id] = var


while token != 'EOF':
    if token not in scanner.tokens:
        if token not in IDs:
            if in_DCL:
                IDs.append(token)
            else:
                print("ID not declared.")
                # exit()
        var = token
        token = 'id'
    print(token, var)
    st = PT_list[state][token].split()

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
