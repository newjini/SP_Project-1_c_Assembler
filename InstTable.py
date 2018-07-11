class InstTable:

    def __init__(self, fileName):
        self.instDic = {}
        self.openFile(fileName)

    def openFile(self, fileName):
        file = open(fileName, 'r')
        lines = file.readlines( )
        for line in lines:
            inst = Instruction(line)
            self.instDic[inst.instruction] = inst
        file.close( )


class Instruction:
    def __init__(self, line):

        self.i_token = None
        self.instruction = ""
        self.opcode = 0
        self.numberOfoperand = 0
        self.format = 0
        self.parsing(line)

    def parsing(self, line):

        i_token = line.split()
#        print(i_token)
        self.instruction = i_token[0]

        if i_token[1] == "3/4":
            self.format = 3
        else:
            self.format = i_token[1]
        self.opcode = (int(i_token[2],16))
        self.numberOfoperand = i_token[3]