import compilee.CompilerScanner as scanner
import csv
import compilee.CodeGenerator as CG

file_name = 'mahsa.txt'
table_name = 'Table_5.csv'
scanner = scanner.Scanner(file_name)
cg = CG.CodeGenerator()
PT_reader = csv.DictReader(open(table_name, 'r'), delimiter=',')
PT_list = []

for row in PT_reader:
    PT_list.append(row)

state = 0
token = scanner.next_token()
parse_stack = []
STable = dict()
STable_reverse = dict()
in_DCL = False
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
    if token > 55:
        var = scanner.STable_reverse[token]
        token = 'id'
    else:
        var = token
        token = scanner.tokens[token]
    print(token)
    state_token = PT_list[state][token]
    st = state_token.split()

    if st[0] == 'REDUCE':
        next_state = parse_stack.pop()
        state = next_state

    elif st[0] == 'PUSH_GOTO':
        parse_stack.append(state)
        next_state = int("".join(list(st[1])[1:]))
        generate_code(st[2], var)
        continue
    elif st[0] == 'SHIFT':
        next_state = int(str(list(st[1])[1:]))
        generate_code(st[2], var)

    else:
        print('Parser Error')
        break

    token = scanner.next_token()

print('Compile done!')
