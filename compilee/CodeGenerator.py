class CodeGenerator:
    def __init__(self):
        self.file = open('mahsa.ll', 'r+')
        self.file.truncate()
        self.temp_num = 0
        self.semantic_stack = []

    def getType(self , a):
        if isinstance(a,int):
            return "i4"
        if isinstance(a,float):
            return "float"

    def getTemp(self) :
        temp = "%" + str(self.temp_num)
        self.temp_num+=1
        return temp


    def push(self,id):
        self.semantic_stack.append(id)

    def sum(self):
        a = self.semantic_stack.pop()
        b = self.semantic_stack.pop()
        if (self.getType(a) == self.getType(b)) or () or ():
            self.file(self.getTemp()+ " =" +"add "+self.getType(a)+" %a, %b")
        else:
            print("Error")





