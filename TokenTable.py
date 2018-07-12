import SymbolTable

class TokenTable:

    ## nixbpe 연산 시 가독성을 위해 클래스 변수 선언 ##
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
        self.i_format = 0  # 해당instruction format
        self.objcode = 0
        self.T_addr = 0
        self.PC_addr = 0
        self.lit = []
        self.tokenList = []
        self.f_opt = 0 # 4형식 operator 처리할 때 사용 , +JSUB, +STCH, +LDX 등
        self.op = ""


    ### 일반 문자열을 받아서 Token단위로 분리시켜 tokenList에 추가하고, locctr 계산 ###
    def putToken(self, line):
        t = Token(line) ## Token 클래스
        self.tokenList.append(t)

        self.f_opt =t.operator
        t.location = self.locctr

        if t.operator=="START" or t.operator=="CSECT": ## START나 CSECT 만나면 locctr 초기화
            self.locctr = 0

        if t.label != "": ## label 심볼테이블에 추가
            self.symtab.putSymbol(t.label, self.locctr)

        if "+" in t.operator: ## 4형식 처리
            self.f_opt = t.operator[1:]
            if self.f_opt in self.insttab.instDic.keys():
                self.i_format = self.insttab.instDic.get(self.f_opt).format
            self.locctr += 4
            t.byteSize += 4

        elif t.operator in self.insttab.instDic.keys(): ## instruction인 operator 처리
            self.i_format = self.insttab.instDic.get(t.operator).format

            if self.i_format == "1": ## format = 1인 operator
                self.locctr += 1
                t.byteSize += 1 ##objectCode 만들 때 길이계산하기 위해 byteSize도 추가

            elif self.i_format == "2": ## format = 2인 operator
                self.locctr += 2
                t.byteSize += 2

            else: ## format = 3인 operator
                self.locctr += 3
                t.byteSize += 3

        elif t.operator == "EQU": ## EQU 처리
            if "-" in t.operand:
                t.operand = t.operand.split("-") ## "-"로 구분하여 locctr 변경해줌
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

        if "=" in t.operand: ## 정수형 리터럴 처리
            if self.littab.search(t.operand)== -1:
                self.littab.putSymbol(t.operand, self.locctr)
                if "X" in t.operand:
                    self.locctr += 1
                    t.byteSize += 1


    ### tokenList에서 index에 해당하는
    ###         Token 리턴         ###
    def getToken(self, index): # index 는 숫자
        return self.tokenList[index]

    ### pass2 과정에서 사용하며, objectCode를 생성함 (token.ObjectCode에 저장) ###
    def makeObjectCode(self, token):
        self.op = self.insttab.instDic.get(self.f_opt)
        self.objcode = 0
        self.format_2 = 0
        self.T_addr = 0
        self.PC_addr = 0

        if "+" in token.operator: ## 4형식일 때 nixbpe 계산하고 objectCode 만들기
            self.f_opt = token.operator[1:]
            self.op = self.insttab.instDic.get(self.f_opt)

            token.setFlag(TokenTable.N_FLAG, 1)
            token.setFlag(TokenTable.I_FLAG, 1)
            token.setFlag(TokenTable.E_FLAG, 1)

            if token.operand[1] == "X": ## operand에 x가 있다면
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
                ## 현재section에 있지않은 symbol이면 objectCode에 0을 넣어줌 ( 값 모르니까 )
                token.objectCode = str.format("%06X" % (self.objcode))

        elif token.operator in self.insttab.instDic.keys(): ## operator가
            self.op = self.insttab.instDic.get(token.operator) ##instruction일 때 기계어 코드 처리
            self.i_format = self.insttab.instDic.get(token.operator).format

            if self.i_format == 3: ## format이 3일 때
                self.objcode = self.op.opcode << 16

                if "#" in token.operand: ## 직접
                    self.T_addr = token.operand[1:]
                    token.setFlag(TokenTable.I_FLAG, 1)
                    self.objcode += token.nixbpe << 12
                    self.objcode += int(self.T_addr)
                    token.objectCode = str.format("%06X" %(self.objcode))

                elif "@" in token.operand: ## 간접
                    token.setFlag(TokenTable.N_FLAG, 1)
                    token.setFlag(TokenTable.P_FLAG, 1)
                    self.objcode += token.nixbpe << 12
                    self.T_addr = self.symtab.search(token.operand[1:])
                    self.PC_addr = self.getToken(self.tokenList.index(token) + 1).location
                    self.objcode += (self.T_addr-self.PC_addr)
                    token.objectCode = str.format("%06X" %(self.objcode))

                elif "=" in token.operand: ## 리터럴부분 처리
                    token.setFlag(TokenTable.N_FLAG,1)
                    token.setFlag(TokenTable.I_FLAG,1)
                    token.setFlag(TokenTable.P_FLAG,1)
                    self.objcode += token.nixbpe << 12
                    token.litSize = len(token.operand.split("'")[1])
                    token.literal = token.operand.split("'")[1][:]

                    if "=C" in token.operand: ##문자열 literal
                        self.lit = token.literal[:]

                        token.literal = ""
                        for i in self.tokenList: ## LTORG가 있을때
                            if i.operator == "LTORG":
                                self.littab.modifySymbol(token.operand, i.location)
                        for a in range(len(self.lit)):
                            token.literal += str.format("%02X" %(ord(self.lit[a])))

                    else: ##정수 literal
                        for i in self.tokenList:
                            if i.operator == "END":
                                self.littab.modifySymbol(token.operand, i.location)
                                i.objectCode = token.literal


                    self.T_addr = self.littab.search(token.operand)
                    self.PC_addr = self.getToken(self.tokenList.index(token)+1).location
                    self.objcode += (self.T_addr - self.PC_addr)

                    token.objectCode = str.format("%06X" %(self.objcode))

                elif token.operand == "": ## operand 가 0 일 때
                    token.setFlag(TokenTable.N_FLAG, 1)
                    token.setFlag(TokenTable.I_FLAG, 1)
                    self.objcode += token.nixbpe << 12
                    token.objectCode = str.format("%06X" %(self.objcode))

                else:                     ## 그 외 일반적인 기계어코드 처리
                    token.setFlag(TokenTable.N_FLAG,1)
                    token.setFlag(TokenTable.I_FLAG,1)
                    token.setFlag(TokenTable.P_FLAG,1)
                    self.objcode += token.nixbpe << 12
                    self.T_addr = self.symtab.search(token.operand) ## Target Address
                    self.PC_addr = self.getToken(self.tokenList.index(token) + 1).location ## PC Address
                    if self.T_addr <= self.PC_addr:

                        self.objcode += ((self.T_addr - self.PC_addr) & 0x00000FFF)+1
                    else:
                        self.objcode += (self.T_addr - self.PC_addr)
                    token.objectCode = str.format("%06X" %(self.objcode))

            else: ## format 2 일때,  각 레지스터에 따른 기계어 코드 처리
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





### 각 라인별로 저장된 코드를 단어 단위로 분할한 후  의미를 해석하는 데에 사용되는 변수와 연산을 정의
### 의미 해석이 끝나면 pass2에서 object code로 변형되었을 때의 바이트 코드 역시 저장
class Token:

    def __init__(self, line):
        ## 의미 분석 단계에서 사용되는 변수 ##
        self.location = 0
        self.literal = []
        self.label = ""
        self.operator = ""
        self.operand = []
        self.comment = ""
        ## object Code 생성 단계에서 사용되는 변수 ##
        self.byteSize = 0
        self.litSize = 0
        self.nixbpe = 0
        self.objectCode = ""

        self.parsing(line)

    ### line의 실질적인 분석 수행 함수, Token의 각 변수에 분석 결과를 저장함 ###
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


    ### n,i,x,b,p,e flag을 설정 ###
    ### nixbpe 연산 시에 사용 ###
    def setFlag(self, flag, value):
        if value == 1:
            self.nixbpe |= flag

    def getFlag(self, flag):
        return self.nixbpe & flag