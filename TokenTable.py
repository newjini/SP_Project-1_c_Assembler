import SymbolTable
import InstTable

class TokenTable:
    N_FLAG = 32
    I_FLAG = 16
    X_FLAG = 8
    B_FLAG = 4
    P_FLAG = 2
    E_FLAG = 1

    def __init__(self, insttab):
        self.symtab = SymbolTable.SymbolTable( )
        self.littab = SymbolTable.SymbolTable( )
        self.insttab = insttab
        self.locctr = 0
        self.addr = 0
        self.i_format = 0 # 해당instruction format
        self.objcode = 0
        self.T_addr = 0
        self.PC_addr = 0
        self.lit = []
        self.tokenList = []
        self.f_opt = 0 # +JSUB, +STCH, +LDX 등
    def putToken(self, line):
        t = Token(line)
        self.tokenList.append(t)

        t.location = self.locctr

        if t.operator=="START" or t.operator=="CSECT":
            self.locctr = 0

        if t.label != "":
            self.symtab.putSymbol(t.label, self.locctr)

        if "+" in t.operator:
            self.f_opt = t.operator[1:]
            if self.f_opt in self.insttab.instDic.keys():
            #     self.i_format = self.insttab.instDic.get(self.f_opt).format
                self.locctr += 4
                t.byteSize += 4

        elif t.operator in self.insttab.instDic.keys():
            self.i_format = self.insttab.instDic.get(t.operator).format
#            print(self.i_format)

            if self.i_format == "1":
                self.locctr += 1
                t.byteSize += 1

            elif self.i_format == "2":
                self.locctr += 2
                t.byteSize += 2

            else:
                self.locctr += 3
                t.byteSize += 3

        elif t.operator == "EQU":
            if "-" in t.operand:
                t.operand = t.operand.split("-")
                loc1 = self.symtab.search(t.operand[0])
                loc2 = self.symtab.search(t.operand[1])
                self.locctr = loc1 - loc2
                self.symtab.modifySymbol(t.label, self.locctr)
                t.location = self.locctr

        elif t.operator == "RESW":
            self.locctr += (3*int(t.operand))

        elif t.operator == "RESB":
            self.locctr += (1*int(t.operand))

        elif t.operator == "BYTE":
            self.locctr +=1
            t.byteSize +=1

        elif t.operator == "WORD":
            self.locctr +=3
            t.byteSize +=3

        elif t.operator == "LTORG":
            self.locctr +=3

        if "=" in t.operand:
            if self.littab.search(t.operand)== "-1":
                self.littab.putSymbol(t.operand, self.locctr)
                if "X" in t.operand:
                    self.locctr += 1
                    t.byteSize += 1
    def getToken(self, index):
        return self.tokenList[index]

    def makeObjectCode(self, index):
        op = self.insttab.instDic.keys(index)
        print(op)





class Token:

    def __init__(self, line):
        self.location = 0
        self.byteSize = 0
        self.litSize = 0
        self.nixbpe = 0
        self.objectCode = ""
        self.literal = ""

        self.label = ""
        self.operator = ""
        self.operand = ""
        self.comment = ""
        self.parsing(line)

    def parsing(self, line):
        l_token = line.split("\t")
        self.label = l_token[0]
        self.operator = l_token[1]

        if "," in l_token[2]:
            # self.operand = []
            self.operand = l_token[2].split(",")

        else:
            self.operand = l_token[2]
        self.comment = l_token[3]



    def setFlag(self, flag, value):
        if value == 1:
            self.nixbpe |= flag

    def getFlag(self, flag):
        return self.nixbpe & flag