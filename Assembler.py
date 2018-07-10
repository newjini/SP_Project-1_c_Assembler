import InstTable
import SymbolTable
import TokenTable

class Assembler:
    def __init__(self, instFile):
        self.section = 999
        self.instTable = InstTable.InstTable(instFile)
        self.tokenTable = TokenTable.TokenTable(self.instTable)
#        self.instTable.openFile()
        self.symtabList = []
        self.literalList = []
        self.tokenList = []
        self.lineList = []
        self.count = 0
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
#            self.tokenList.append(TokenTable.TokenTable(self.instTable))
            self.tokenTable.putToken(str(i))
            self.count += 1

    def pass2(self):
        self.output = ""
        self.H_code = ""
        self.T_code = ""
        self.M_code = ""
        self.E_code = ""
        self.lit_code = ""
        self.loc = ""
        self.leng = ""
        self.total_leng = 0
        self.end = 0
        
        for i in range(self.count):
#            self.tokenTable.makeObjectCode(self.tokenTable.getToken(i).operator)
            self.tokenTable.makeObjectCode(self.tokenTable.getToken(i))










if __name__ == '__main__':
    assembler = Assembler("inst.data")
    assembler.loadInputFile("input.txt")
    assembler.pass1()

    # assembler.printSymbolTable("symtab_20160273.txt");
    #
    assembler.pass2();
    # assembler.printObjectCode("output_20160273.txt");