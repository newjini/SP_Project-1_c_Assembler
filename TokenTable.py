import SymbolTable

class TokenTable:
    N_FLAG = 32
    I_FLAG = 16
    X_FLAG = 8
    B_FLAG = 4
    P_FLAG = 2
    E_FLAG = 1

    def __init__(self, insttab, section):
        self.section = section
        self.symtab = SymbolTable.SymbolTable(self.section)
        self.littab = SymbolTable.SymbolTable(self.section)
        self.insttab = insttab
        self.locctr = 0
        self.i_format = 0 # 해당instruction format
        self.objcode = 0
        self.T_addr = 0
        self.PC_addr = 0
        self.lit = []
        self.tokenList = []
        self.f_opt = 0 # +JSUB, +STCH, +LDX 등
        self.op = ""



    def putToken(self, line):
        t = Token(line)
        self.tokenList.append(t)

        self.f_opt =t.operator
        t.location = self.locctr

        if t.operator=="START" or t.operator=="CSECT":
            self.locctr = 0

        if t.label != "":
            self.symtab.putSymbol(t.label, self.locctr)

        if "+" in t.operator:
            self.f_opt = t.operator[1:]
            if self.f_opt in self.insttab.instDic.keys():
                self.i_format = self.insttab.instDic.get(self.f_opt).format
            self.locctr += 4
            t.byteSize += 4

        elif t.operator in self.insttab.instDic.keys():
            self.i_format = self.insttab.instDic.get(t.operator).format

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
            if self.littab.search(t.operand)== -1:
                self.littab.putSymbol(t.operand, self.locctr)
                if "X" in t.operand:
                    self.locctr += 1
                    t.byteSize += 1



    def getToken(self, index): # index 는 숫자
        return self.tokenList[index]

    def makeObjectCode(self, token):
        self.op = self.insttab.instDic.get(self.f_opt)
        self.objcode = 0
        self.format_2 = 0
        self.T_addr = 0
        self.PC_addr = 0

        if "+" in token.operator:
            self.f_opt = token.operator[1:]
            self.op = self.insttab.instDic.get(self.f_opt)

            token.setFlag(TokenTable.N_FLAG, 1)
            token.setFlag(TokenTable.I_FLAG, 1)
            token.setFlag(TokenTable.E_FLAG, 1)

            if token.operand[1] == "X":
                token.setFlag(TokenTable.X_FLAG, 1)

            self.objcode += self.op.opcode << 24
            self.objcode += token.nixbpe << 20
            token.objectCode = str.format("%08X" %(self.objcode))

        elif token.operator == "BYTE":
            token.objectCode = token.operand.split("'")[1]

        elif token.operator == "WORD":
            self.a = self.symtab.search(token.operand[0])
            self.b = self.symtab.search(token.operand[1])
            if self.a==-1 and self.b==-1:
                self.objcode = 0
                token.objectCode = str.format("%06X" % (self.objcode))

        elif token.operator in self.insttab.instDic.keys():
            self.op = self.insttab.instDic.get(token.operator)
            self.i_format = self.insttab.instDic.get(token.operator).format

            if self.i_format == 3:
                self.objcode = self.op.opcode << 16
                if "#" in token.operand:
                    self.T_addr = token.operand[1:]
                    token.setFlag(TokenTable.I_FLAG, 1)
                    self.objcode += token.nixbpe << 12
                    self.objcode += int(self.T_addr)
                    token.objectCode = str.format("%06X" %(self.objcode))
                elif "@" in token.operand:

                    token.setFlag(TokenTable.N_FLAG, 1)
                    token.setFlag(TokenTable.P_FLAG, 1)
                    self.objcode += token.nixbpe << 12
                    self.T_addr = self.symtab.search(token.operand[1:])
                    self.PC_addr = self.getToken(self.tokenList.index(token) + 1).location
                    self.objcode += (self.T_addr-self.PC_addr)
                    token.objectCode = str.format("%06X" %(self.objcode))
                elif "=" in token.operand:

                    token.setFlag(TokenTable.N_FLAG,1)
                    token.setFlag(TokenTable.I_FLAG,1)
                    token.setFlag(TokenTable.P_FLAG,1)
                    self.objcode += token.nixbpe << 12
                    token.litSize = len(token.operand.split("'")[1])
                    token.literal = token.operand.split("'")[1][:]

                    if "=C" in token.operand:
                        self.lit = token.literal[:]

                        token.literal = ""
                        for i in self.tokenList:
                            if i.operator == "LTORG":
                                self.littab.modifySymbol(token.operand, i.location)
                        for a in range(len(self.lit)):
                            token.literal += str.format("%02X" %(ord(self.lit[a])))

                    else:
                        for i in self.tokenList:
                            if i.operator == "END":
                                self.littab.modifySymbol(token.operand, i.location)
                                i.objectCode = token.literal


                    self.T_addr = self.littab.search(token.operand)
                    self.PC_addr = self.getToken(self.tokenList.index(token)+1).location
                    self.objcode += (self.T_addr - self.PC_addr)

                    token.objectCode = str.format("%06X" %(self.objcode))



                elif token.operand == "":
                    token.setFlag(TokenTable.N_FLAG, 1)
                    token.setFlag(TokenTable.I_FLAG, 1)
                    self.objcode += token.nixbpe << 12
                    token.objectCode = str.format("%06X" %(self.objcode))
                else:
                    token.setFlag(TokenTable.N_FLAG,1)
                    token.setFlag(TokenTable.I_FLAG,1)
                    token.setFlag(TokenTable.P_FLAG,1)
                    self.objcode += token.nixbpe << 12
                    self.T_addr = self.symtab.search(token.operand)
                    self.PC_addr = self.getToken(self.tokenList.index(token) + 1).location
                    if self.T_addr <= self.PC_addr:

                        self.objcode += ((self.T_addr - self.PC_addr) & 0x00000FFF)+1
                    else:
                        self.objcode += (self.T_addr - self.PC_addr)
                    token.objectCode = str.format("%06X" %(self.objcode))
            else:
                for i in range(len(token.operand)):
                    if token.operand[i] == "A":
                        self.format_2 |= 0
                    elif token.operand[i] == "X":
                        self.format_2 |= 1
                    elif token.operand[i] == "L":
                        self.format_2 |= 2
                    elif token.operand[i] == "B":
                        self.format_2 |= 3
                    elif token.operand[i] == "S":
                        self.format_2 |= 4
                    elif token.operand[i] == "T":
                        self.format_2 |= 5
                    elif token.operand[i] == "F":
                        self.format_2 |= 6
                    elif token.operand[i] == "PC":
                        self.format_2 |= 8
                    elif token.operand[i] == "SW":
                        self.format_2 |= 9
                    if i == 0:
                        self.format_2 = self.format_2 << 4
                token.objectCode = str.format("%02X%02X" %(self.op.opcode, self.format_2))
 #       print(self.symtab.search("MAXLEN"))
 #       print(token.objectCode)





class Token:

    def __init__(self, line):
        self.location = 0
        self.byteSize = 0
        self.litSize = 0
        self.nixbpe = 0
        self.objectCode = ""
        self.literal = []

        self.label = ""
        self.operator = ""
        self.operand = []
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