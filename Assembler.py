import InstTable
import SymbolTable
import TokenTable

class Assembler:
    def __init__(self, instFile):
        self.section = 999
        self.instTable = InstTable.InstTable(instFile)
#        self.instTable.openFile()
        self.symtabList = []
        self.literalList = []
        self.tokenList = []
        self.lineList = []
    def loadInputFile(self, inputFile):
        f = open(inputFile, 'r')
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
            TokenTable.TokenTable(self.instTable).putToken(str(i))





if __name__ == '__main__':
    assembler = Assembler("inst.data")
    assembler.loadInputFile("input.txt")
    assembler.pass1()

    # assembler.printSymbolTable("symtab_20160273.txt");
    #
    # assembler.pass2();
    # assembler.printObjectCode("output_20160273.txt");