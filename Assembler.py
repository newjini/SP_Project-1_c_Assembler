import InstTable
import SymbolTable
import TokenTable

class Assembler:
    def __init__(self, instFile):
        self.section = 999
        self.instTable = InstTable.InstTable(instFile)
#        self.tokenTable = TokenTable.TokenTable(self.instTable, self.section)
        self.codeList = []
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
                self.tokenList.append(self.tokenTable)

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
        self.leng = 0
        self.total_leng = 0
        self.end = 0
        self.count = 0 # modification code 작성 시 0의 개수 세는 변수
        self.lit = []

        for i in self.tokenList:
            for j in range(len(i.tokenList)):
                t = i.getToken(j)
                i.makeObjectCode(t)
                if t.operator == "START" or t.operator == "CSECT":
                    self.H_code = "H" + t.label + "\t" + str.format("%06X" % (t.location))

                    if t.operator == "START":
                        self.loc = str.format("%06X" % (i.getToken(-2).location))
                        self.E_code = "E"+  str.format("%06X" % (t.location))+"\n"
                    else:
                        self.loc = str.format("%06X" % (i.locctr))
                        self.E_code = "E"+"\n"
                    self.H_code += self.loc

                elif t.operator == "EXTDEF":
                    self.H_code += "\nD"
                    for a in range(len(t.operand)):
                        self.loc = str.format("%06X" % (i.symtab.search(t.operand[a])))
                        self.H_code += t.operand[a] + self.loc

                elif t.operator == "EXTREF":
                    self.H_code += "\nR"
                    for a in range(len(t.operand)):
                        self.H_code += t.operand[a]
                    self.H_code += "\n"
                elif "+" in t.operator:
                    self.loc = str.format("%06X" %(t.location+1))
                    self.count = t.objectCode.count('0')
                    if len(t.operand) == 2:
                        t.operand = t.operand[0]
                    self.M_code += "M" + self.loc + str.format("%02X" %(self.count)) + "+" + t.operand + "\n"

                elif t.operator == "WORD":
                    self.loc = str.format("%06X" %(t.location))
                    self.count = t.objectCode.count('0')
                    t.operand = t.operand.split("-")
                    self.M_code += "M" + self.loc + str.format("%02X" %(self.count)) + "+" + t.operand[0]+"\n"
                    self.M_code += "M" + self.loc + str.format("%02X" %(self.count)) + "-" + t.operand[0]+"\n"

                elif t.location == 0 and t.objectCode != "" :

                    self.loc = str.format("%06X" %(t.location))
                    self.output += "T"+self.loc
                    for m in range(len(i.tokenList)):
                        tt = i.getToken(m)
                        i.makeObjectCode(tt)
                        self.leng = tt.byteSize

                        if self.total_leng + self.leng > 30:
                            self.output += str.format("%02X" %(self.total_leng)) + self.T_code
                            self.total_leng = 0
                            self.loc = str.format("%06X" %(tt.location))
                            self.output += "\nT"+self.loc
                            self.T_code = ""
                        self.total_leng += self.leng
                        self.T_code += tt.objectCode
                    self.output += str.format("%02X" %(self.total_leng)) + self.T_code +"\n"

                elif "=" in t.operand:
                    for a in range(len(i.tokenList)):
                        if i.littab.search(t.operand) != -1:
                            self.litloc = i.littab.search(t.operand)
                            break
                    for b in range(len(i.tokenList)):
                        if self.litloc == i.getToken(b).location and self.litloc != 0:
                            if "=C" in t.operand:
                                self.lit_code += "T" + str.format("%06X" %self.litloc)+str.format("%02X" %t.litSize)+t.literal+"\n"



            self.codeList.append(self.H_code+self.output+self.lit_code+self.M_code+self.E_code)

            self.output = ""
            self.M_code = ""
            self.T_code = ""
            self.total_leng = 0
            self.litloc = ""
            self.lit_code = ""
            self.E_code = ""

        # for a in range(len(t.literal)):
        #     self.lit += t.literal[a]
        #     print(self.lit[a])
        #     self.lit = str.format("%02X" %(ord(self.lit[a])))
        #     print(self.lit)

        # self.lit += str.format("%02X" % (ord(t.literal[a])))
        # t.literal = self.lit
        # self.lit = ""
        # print(t.literal)








if __name__ == '__main__':
    assembler = Assembler("inst.data")
    assembler.loadInputFile("input.txt")
    assembler.pass1()

    # assembler.printSymbolTable("symtab_20160273.txt");
    #
    assembler.pass2();
    # assembler.printObjectCode("output_20160273.txt");