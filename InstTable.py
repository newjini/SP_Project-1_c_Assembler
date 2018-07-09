class InstTable:

    def __init__(self):
        self.instDic = {}

    def openFile(self, fileName):
        file = open(fileName, 'r')
        lines = file.readlines()
        for line in lines:
            inst = line.split()[0]
            self.instDic[inst] = line.split()[1:]
            Instruction.parsing(self, line)
        file.close()

class Instruction:
    def __init__(self):
        # self.instruction = instruction
        # self.opcode = opcode
        # self.numberOfoperand = numberOfoperand
        # self.format = format
        self.instruction = ""
        self.opcode = None
        self.numberOfoperand = None
        self.format = None
        self.parsing()

    def parsing(self,line):
        self.instruction = line.split()[0]
        if line.split()[1] == "3/4" :
            self.format = 3
        else :
            self.format = line.split()[1]
        self.opcode = line.split()[2]
        self.numberOfoperand = line.split()[3]
