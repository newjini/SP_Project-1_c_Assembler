import InstTable
import SymbolTable
import TokenTable

class Assembler:
    def __init__(self, instFile):
        self.section = 999
        self.instTable = InstTable.InstTable()
        self.instTable.openFile(instFile)
        self.symtabList = []
        self.literalList = []
        self.tokenList = []
        self.lineList = []
    def loadInputFile(self, inputFile):
        f = open("input.txt", 'r')
        lines = f.readlines()
        for line in lines:
            self.lineList.append(line)
    def pass1(self):
        for i in self.lineList:
            if '.' in i:
                continue
            p_label = i.split()
            if 'START' in p_label:
                self.section = 0
            elif 'CSECT' in p_label:
                self.section+=1
            self.symtabList.append(self.section)
            self.literalList.append(self.section)
#            self.tokenList.append(self.symtabList,  self.instTable, self.literalList)
            TokenTable.TokenTable().putToken(str(i))





if __name__ == '__main__':
    assembler = Assembler("inst.data")
    assembler.loadInputFile("input.txt")
    assembler.pass1()

    # assembler.printSymbolTable("symtab_20160273.txt");
    #
    # assembler.pass2();
    # assembler.printObjectCode("output_20160273.txt");




# lineList = []
#
# def loadInput(): # input.txt load 하는 부분
#     f = open("input.txt", 'r')
#     lines = f.readlines()
#     for line in lines:
#         lineList.append(line.split("\n"))
#     f.close()
# def pass1(): # 토큰단위로 분리하고 토큰테이블 생성
#     str = list()
#     label = list()
#     operator = list()
#     op = list()
#     opp = list()
#     operand = list()
#     comment = list()
#     i_line = list()
#     for i in lineList:
# #        i_line = lineList.index()
#         str = '\t'.join(i)
#         str_token = str.split("\t")
#         label.append(str_token[0])
#         operator.append(str_token[1])
#         comment.append(str_token[3:])
#         op.append(str_token[2])
#         opp = ','.join(op)
#         oppp = opp.split(",")
#
#
#
# #        label= str_token[0]
