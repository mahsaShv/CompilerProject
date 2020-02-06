class CodeGenerator:
    def __init__(self):
        self.file = open('mahsa.llvm', 'r+')
        self.file.truncate()

    def getType(self , a):
        if isinstance(a,int):
            return "i4"
        if isinstance(a,float):
            return "float"

    def getTemp(self) :
        pass



    def sum(self, a , b ):
        if (self.getType(a) == self.getType(b)) or () or ():
            self.file("add "+self.getType(a)+" %a, %b")

        else:
            print("Error")





