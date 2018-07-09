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
        self.loc1 = 0
        self.loc2 = 0
        self.tokenList.append(line)

        t = Token(line)

        t.location = self.locctr

        if t.operator=="START" or t.operator=="CSECT":
            self.locctr = 0
        if t.label != "":
            self.symtab.putSymbol(t.label, self.locctr)
        if "+" in t.operator:
            self.f_opt = t.operator[1:]
            if self.f_opt in self.insttab.instDic.keys():
                self.insttab.instDic.get(self.f_opt)
                print(self.insttab.instDic.get(self.f_opt).format)




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