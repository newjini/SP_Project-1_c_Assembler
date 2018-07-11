import InstTable
import SymbolTable
import TokenTable

class Assembler:
    def __init__(self, instFile):
        self.section = 999
        self.instTable = InstTable.InstTable(instFile)
#        self.tokenTable = TokenTable.TokenTable(self.instTable, self.section)

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
                self.symTab = SymbolTable.SymbolTable(self.section)
                self.symtabList.append(self.symTab.section)
                self.literalList.append(self.symTab.section)
                self.tokenTable = TokenTable.TokenTable(self.instTable, self.symTab.section)

            elif 'CSECT' in p_label:
                self.section+=1
                self.symTab = SymbolTable.SymbolTable(self.section)
                self.symtabList.append(self.symTab.section)
                self.literalList.append(self.symTab.section)
                self.tokenTable = TokenTable.TokenTable(self.instTable, self.symTab.section)

            self.tokenList.append(self.tokenTable)
            self.tokenTable.putToken(str(i))


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
        self.count = 0
        self.count2 = 0
        self.count3 = 0
        for i in self.tokenList:
            if i.section==0:
                i.makeObjectCode(i.getToken(self.count))
                self.count += 1
            elif i.section==1:
                i.makeObjectCode(i.getToken(self.count2))
                self.count2 += 1
            else:
                i.makeObjectCode(i.getToken(self.count3))
                self.count3 += 1








if __name__ == '__main__':
    assembler = Assembler("inst.data")
    assembler.loadInputFile("input.txt")
    assembler.pass1()

    # assembler.printSymbolTable("symtab_20160273.txt");
    #
    assembler.pass2();
    # assembler.printObjectCode("output_20160273.txt");