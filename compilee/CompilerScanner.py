import re


class Scanner:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.line_index = 0
        self.char_index = 0

        try:
            self.file = open(file_name, "r")
            self.text = self.file.readlines()
        except IOError:
            print("File not accessible")
        finally:
            self.file.close()

        self.KWTable = {
            "function": 0,
            "begin": 1,
            "return": 2,
            "end": 3,
            "procedure": 4,
            "boolean": 5,
            "integer": 6,
            "character": 7,
            "real": 8,
            "string": 9,
            "main": 10,
            "read": 11,
            "write": 12,
            "strlen": 13,
            "if": 14,
            "then": 15,
            "else": 16,
            "while": 17,
            "do": 18,
            "and": 19,
            "or": 20,
            "assign": 21,
            "break": 22,
            "char": 23,
            "continue": 24,
            "false": 25,
            "true": 26,
            "of": 27,
            "var": 28,
            "long": 29
        }

        self.specialTTable = {

            ')': 30,
            ':': 31,
            ';': 32,
            ',': 33,
            '=': 34,
            '+': 35,
            '-': 36,
            '*': 37,
            '/': 38,
            '&': 39,
            '^': 40,
            '|': 41,
            '%': 42,
            '~': 43,
            '<': 44,
            '<=': 45,
            '>': 46,
            '>=': 47,
            '<>': 48,
            '--': 49,
            '<--': 50,
            '-->': 51,
            '\'': 52,
            '\"': 53,
            '(': 54,
            ':=': 55,
        }

        self.tokens = {
            0: "function",
            1: "begin",
            2: "return",
            3: "end",
            4: "procedure",
            5: "boolean",
            6: "integer",
            7: "character",
            8: "real",
            9: "string",
            10: "main",
            11: "read",
            12: "write",
            13: "strlen",
            14: "if",
            15: "then",
            16: "else",
            17: "while",
            18: "do",
            19: "and",
            20: "or",
            21: "assign",
            22: "break",
            23: "char",
            24: "continue",
            25: "false",
            26: "true",
            27: "of",
            28: "var",
            29: "long",

            30: ')',
            31: ':',
            32: ';',
            33: ',',
            34: '=',
            35: '+',
            36: '-',
            37: '*',
            38: '/',
            39: '&',
            40: '^',
            41: '|',
            42: '%',
            43: '~',
            44: '<',
            45: '<=',
            46: '>',
            47: '>=',
            48: '<>',
            49: '--',
            50: '<--',
            51: '-->',
            52: '\'',
            53: '\"',
            54: '(',
            55: ':=',

        }

        self.stp = 0
        self.STable = dict()

    def next_char(self):
        if self.char_index == len(self.text[self.line_index]):
            self.line_index += 1
            self.char_index = 0
            if self.line_index == len(self.text):
                return '$'
            char = self.text[self.line_index][self.char_index]
        else:
            char = self.text[self.line_index][self.char_index]
            self.char_index += 1
        return char

    def go_to_prev_char(self):
        if self.char_index == 0:
            self.line_index -= 1
            self.char_index = len(self.text[self.line_index])

        else:
            self.char_index -= 1

    def next_token(self):
        string = ""
        char = self.next_char()
        string += char
        word_index = self.char_index

        while True:
            if char == '$':
                return "EOF"
            # if self.isWhiteSpace(char):
            #     continue

            if re.search("^[a-zA-Z]", char):
                char = self.next_char()

                while True:
                    if re.search("[a-zA-Z|_|0-9]", char):
                        string += char
                        char = self.next_char()
                    else:
                        self.go_to_prev_char()
                        if string in self.KWTable:
                            return self.KWTable[string]
                        else:
                            # self.STable[self.stp] =
                            # TODO
                            return string

            if re.search("^[0-9]", char):
                char = self.next_char()
                if re.search("x", char):
                    pass
                else:
                    while True:
                        if re.search("[0-9]", char):
                            string += char
                            char = self.next_char()
                        else:
                            self.go_to_prev_char()
                            return string
                            # TODO

            if re.search("^\)|^;|^,|^=|^\+|^\*|^/|^&|^^|^\||^%|^~|^\(", char):
                return self.specialTTable[char]

            if re.search("^\'", char):
                print(char)

            char = self.next_char()

            #
            # if string in self.KWTable:
            #     pass

    def isWhiteSpace(self, c):
        if ord(c) == 32 or ord(c) == 10 or ord(c) == 12 or ord(c) == 13 or ord(c) == 9 or ord(c) == 11:
            return True
        return False

    def isID(self, s: str):
        if not re.search("^[a-zA-Z]", s):
            return False
        if re.search("[^a-zA-Z|_|0-9]", s):
            return False
        return True
