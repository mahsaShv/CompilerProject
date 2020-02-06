import compilee.CompilerScanner as scanner
import csv

file_name = 'mahsa.txt'
table_name = 'Table_5.csv'
scanner = scanner.Scanner(file_name)
PT_reader = csv.DictReader(open(table_name, 'r'), delimiter=',')
PT_list = []

for row in PT_reader:
    PT_list.append(row)

state = 0
token = scanner.next_token()
parse_stack = []


def generate_code(func_name):
    if func_name == 'NoSem':
        return


while token != 'EOF':
    token = scanner.tokens[token]
    state_token = PT_list[state][token]
    st = state_token.split()
    if st[0] == 'REDUCE':
        next_state = parse_stack.pop()
        state = next_state
    elif st[0] == 'PUSH_GOTO':
        parse_stack.append(state)
        next_state = int(str(list(st[1])[1:]))
        generate_code(st[2])
    elif st[0] == 'SHIFT':
        next_state = int(str(list(st[1])[1:]))
        generate_code(st[2])
    else:
        print('Error')
        break
    token = scanner.next_token()

print('Compile done!')
