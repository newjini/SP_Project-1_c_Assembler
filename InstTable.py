class InstTable:

    def __init__(self, fileName):
        self.instDic = {}
        self.openFile(fileName)

    def openFile(self, fileName):
        file = open(fileName, 'r')
        lines = file.readlines( )
        for line in lines:
            #            inst = line.split()[0]
            inst = Instruction(line)

            self.instDic[inst.instruction] = inst

        #            self.instDic[inst.instruction] = line.split()[1:]
        file.close( )


class Instruction:
    def __init__(self, line):

        self.i_token = None
        self.instruction = ""
        self.opcode = None
        self.numberOfoperand = None
        self.format = None
        self.parsing(line)

    def parsing(self, line):
        i_token = line.split( )
        self.instruction = i_token[0]

        if i_token[1] == "3/4":
            self.format = 3
        else:
            self.format = i_token[1]
        self.opcode = i_token[2]
        self.numberOfoperand = i_token[3]