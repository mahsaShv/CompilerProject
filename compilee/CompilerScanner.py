import re
import numpy as np
import struct

class Scanner:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.line_index = 0
        self.char_index = 0
        self.getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

        try:
            self.file = open(file_name, "r")
            self.text = self.file.readlines()
        except IOError:
            print("File not accessible")
        finally:
            self.file.close()

        self.KWTable = {
            "function": 'function',
            "begin": 'begin',
            "return": 'return',
            "end": 'end',
            "procedure": 'procedure',
            "boolean": 'boolean',
            "integer": 'integer',
            "character": 'character',
            "real": 'real',
            "string": 'string',
            "main": 'main',
            "read": 'read',
            "write": 'write',
            "strlen": 'strlen',
            "if": 'if',
            "then": 'then',
            "else": 'else',
            "while": 'while',
            "do": 'do',
            "and": 'and',
            "or": 'or',
            "assign": 'assign',
            "break": 'break',
            "char": 'char',
            "continue": 'continue',
            "false": 'false',
            "true": 'true',
            "of": 'of',
            "var": 'var',
            "long": 'long'
        }

        self.specialTTable = {

            ')': ')',
            ':': ':',
            ';': ';',
            ',': ',',
            '=': '=',
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '&': '&',
            '^': '^',
            '|': '|',
            '%': '%',
            '~': '~',
            '<': '<',
            '<=': '<=',
            '>': '>',
            '>=': '>=',
            '<>': '<>',
            '--': '--',
            '<--': '<--',
            '-->': '-->',
            '\'': '\'',
            '\"': '\"',
            '(': '(',
            ':=': ':=',
        }

        self.stp = 56
        self.tokens = {
            "function": 'function',
            "begin": 'begin',
            "return": 'return',
            "end": 'end',
            "procedure": 'procedure',
            "boolean": 'boolean',
            "integer": 'integer',
            "character": 'character',
            "real": 'real',
            "string": 'string',
            "main": 'main',
            "read": 'read',
            "write": 'write',
            "strlen": 'strlen',
            "if": 'if',
            "then": 'then',
            "else": 'else',
            "while": 'while',
            "do": 'do',
            "and": 'and',
            "or": 'or',
            "assign": 'assign',
            "break": 'break',
            "char": 'char',
            "continue": 'continue',
            "false": 'false',
            "true": 'true',
            "of": 'of',
            "var": 'var',
            "long": 'long',
            ')': ')',
            ':': ':',
            ';': ';',
            ',': ',',
            '=': '=',
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '&': '&',
            '^': '^',
            '|': '|',
            '%': '%',
            '~': '~',
            '<': '<',
            '<=': '<=',
            '>': '>',
            '>=': '>=',
            '<>': '<>',
            '--': '--',
            '<--': '<--',
            '-->': '-->',
            '\'': '\'',
            '\"': '\"',
            '(': '(',
            ':=': ':=',
        }

        self.stp = 56
        self.STable = dict()
        self.STable_reverse = dict()

    def next_char(self):
        if self.char_index == len(self.text[self.line_index]):
            self.line_index += 1
            self.char_index = 0
            if self.line_index == len(self.text):
                return '$'
            char = self.text[self.line_index][self.char_index]
            self.char_index += 1
        else:
            char = self.text[self.line_index][self.char_index]
            self.char_index += 1

        return char

    def go_to_prev_char(self):
        if self.char_index == 0:
            self.line_index -= 1
            self.char_index = len(self.text[self.line_index]) - 1
            char = self.text[self.line_index][self.char_index]

        else:
            self.char_index -= 1
            char = self.text[self.line_index][self.char_index]

        return char

    def next_token(self):
        string = ""
        char = self.next_char()
        string += char

        while True:
            if char == '$':
                return "EOF"

            if self.isWhiteSpace(char):
                char = self.next_char()
                while self.isWhiteSpace(char):
                    char = self.next_char()

                # if string[0] == "\n":
                #     char = self.next_char()

                # string = string[1:]
                # string += char
                string = '' + char

            if re.search("^[a-zA-Z]", char):
                char = self.next_char()
                while True:
                    if re.search("[a-zA-Z|_|0-9]", char):
                        string += char
                        char = self.next_char()
                    else:
                        self.go_to_prev_char()
                        if string in self.KWTable:
                            # char = self.next_char()
                            return self.KWTable[string]
                        else:
                            # self.STable.update({string: self.stp})
                            # self.STable_reverse.update({self.stp: string})
                            # self.stp = len(self.STable) + 56
                            # return self.STable[string]
                            return string
            if re.search("^[0-9]", char):
                char = self.next_char()
                if re.search("x", char):
                    string += char
                    char = self.next_char()
                    while True:
                        # char = self.next_char()

                        if re.search("[0-9|a-f]", char):
                            string += char
                            char = self.next_char()
                        else:
                            self.go_to_prev_char()
                            # self.STable.update({string: self.stp})
                            # self.STable_reverse.update({self.stp: string})
                            self.stp += 1
                            temp = np.int32(hex(int(string,base=0)))

                            string = str(np.binary_repr(temp))

                            return string

                else:
                    while True:
                        if re.search("[0-9|.]", char):
                            string += char
                            char = self.next_char()
                        else:
                            self.go_to_prev_char()
                            # self.STable.update({string: self.stp})
                            # self.STable_reverse.update({self.stp: string})
                            self.stp += 1

                            if "." in string:
                                string = str(self.floatToBinary64(float(string)))

                            else:
                                string = str(np.binary_repr(int(string)))

                            return string

            if re.search("^\)|^;|^,|^=|^\+|^\*|^/|^&|^\^|^\||^%|^~|^\(|^\'|^\"", char):
                temp = char
                # char = self.next_char()
                return self.specialTTable[temp]

            if re.search("^<", char):
                temp1 = char
                char = self.next_char()
                temp2 = char

                if char == '=':
                    # char = self.next_char()
                    return self.specialTTable[temp1 + temp2]

                elif char == '>':
                    return self.specialTTable[temp1 + temp2]

                elif char == "-":
                    char = self.next_char()
                    if char == "-":
                        while True:
                            char = self.next_char()
                            if char == "-":
                                char = self.next_char()
                                if char == "-":
                                    char = self.next_char()
                                    if char == ">":
                                        char = self.next_char()
                                        break
                else:
                    char = self.go_to_prev_char()
                    return self.specialTTable[temp1]

            if re.search("^>", char):
                temp1 = char
                char = self.next_char()
                temp2 = char

                if char == '=':
                    return self.specialTTable[temp1 + temp2]
                else:
                    char = self.go_to_prev_char()

                    return self.specialTTable[temp1]

            if re.search("^:", char):
                temp1 = char
                char = self.next_char()
                temp2 = char

                if char == '=':
                    return self.specialTTable[temp1 + temp2]
                else:
                    char = self.go_to_prev_char()
                    return self.specialTTable[temp1]

            if re.search("^-", char):
                temp1 = char
                char = self.next_char()
                temp2 = char

                if char == '-':
                    while True:
                        if char == '\n':
                            # print("break")
                            break
                        char = self.next_char()
                else:
                    char = self.go_to_prev_char()
                    return self.specialTTable[temp1]

    def isWhiteSpace(self, c):
        if '\t' == c or ' ' == c or '\n' == c or '\f' == c or '\r' == c or '\v' == c:
            return True
        return False


    def floatToBinary64(self,value):
        val = struct.unpack('Q', struct.pack('d', value))[0]
        return self.getBin(val)

    def isID(self, s: str):
        if not re.search("^[a-zA-Z]", s):
            return False
        if re.search("[^a-zA-Z|_|0-9]", s):
            return False
        return True

# TODO indent kar nemikone
