import SymbolTable
import InstTable

class TokenTable:
    N_FLAG = 32
    I_FLAG = 16
    X_FLAG = 8
    B_FLAG = 4
    P_FLAG = 2
    E_FLAG = 1

    def __init__(self, symtab, insttab, littab):
        self.symtab = SymbolTable.SymbolTable( )
        self.littab = SymbolTable.SymbolTable( )
        self.insttab = InstTable.InstTable( )
        self.locctr = 0
        self.addr = 0
        self.i_format = 0
        self.objcode = 0
        self.T_addr = 0
        self.PC_addr = 0
        self.lit = []
        self.tokenList = []
    def putToken(self, line):
        self.loc1 = 0
        self.loc2 = 0
        self.tokenList.append(line)
        t = Token
        t.nixbpe = 3


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
        l_token = line.split()
        label = l_token[0]
        operator = l_token[1]
        if "," in l_token[2]:
            operand = l_token[2].split(",")
        else:
            operand = l_token[2]
        comment = l_token[3]

    def setFlag(self, flag, value):
        if value == 1:
            self.nixbpe |= flag

    def getFlag(self, flag):
        return self.nixbpe & flag










