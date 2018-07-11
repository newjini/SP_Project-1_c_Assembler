import InstTable
import SymbolTable
import TokenTable

class Assembler:
    def __init__(self, instFile):
        self.section = 999
        self.length = 0
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
                self.tokenList.append(self.tokenTable)


            elif 'CSECT' in p_label:
                self.section+=1
                self.symTab = SymbolTable.SymbolTable(self.section)
                self.symtabList.append(self.symTab.section)
                self.literalList.append(self.symTab.section)
                self.tokenTable = TokenTable.TokenTable(self.instTable, self.symTab.section)
                self.tokenList.append(self.tokenTable)

            self.length += 1
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
            for j in range(len(i.tokenList)):
                t = i.getToken(j)
                i.makeObjectCode(t)
                if t.operator == "START" or t.operator == "CSECT":
                    self.H_code = "H" + t.label + "\t" + str.format("%06X" % (t.location))
                    if t.operator == "START":
                        self.loc = str.format("%06X" % (i.getToken(-2).location))
                    else:
                        self.loc = str.format("%06X" % (i.locctr))
                    self.H_code += self.loc
                    continue
                elif t.operator == "EXTDEF":
                    self.H_code += "\nD"
                    for a in range(len(t.operand)):
                        self.loc = str.format("%06X" % (i.symtab.search(t.operand[a])))
                        self.H_code += t.operand[a] + self.loc
                    continue
                elif t.operator == "EXTREF":
                    self.H_code += "\nR"
                    for a in range(len(t.operand)):
                        self.H_code += t.operand[a]
                    self.H_code += "\n"
                    continue
            print(self.H_code)







        # for i in self.tokenList:
        #     t = None
        #     if i.section==0:
        #         t = i.getToken(self.count)
        #         i.makeObjectCode(t)
        #         self.count += 1
        #     elif i.section==1:
        #         t = i.getToken(self.count2)
        #         i.makeObjectCode(t)
        #         self.count2 += 1
        #     else:
        #         t = i.getToken(self.count3)
        #         i.makeObjectCode(t)
        #         self.count3 += 1
        #     if t.operator == "START" or t.operator == "CSECT":
        #         self.H_code ="H"+t.label+"\t"+str.format("%06X" %(t.location))
        #         if t.operator =="START":
        #             self.loc = str.format("%06X" %(i.getToken(-2).location))
        #         else:
        #             self.loc = str.format("%06X" %(i.locctr))
        #         self.H_code += self.loc
        #         continue
        #     elif t.operator == "EXTDEF":
        #         self.H_code += "\nD"
        #         for a in range(len(t.operand)):
        #             self.loc = str.format("%06X" %(i.symtab.search(t.operand[a])))
        #             self.H_code += t.operand[a] + self.loc
        #         continue
        #     elif t.operator == "EXTREF":
        #         self.H_code += "\nR"
        #         for a in range(len(t.operand)):
        #             self.H_code += t.operand[a]
        #         self.H_code +="\n"
        #         continue
        #
        #
        #     print(self.H_code)





#            print(i.getToken(-2).location)









if __name__ == '__main__':
    assembler = Assembler("inst.data")
    assembler.loadInputFile("input.txt")
    assembler.pass1()

    # assembler.printSymbolTable("symtab_20160273.txt");
    #
    assembler.pass2();
    # assembler.printObjectCode("output_20160273.txt");