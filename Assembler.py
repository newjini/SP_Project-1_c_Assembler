import InstTable
import SymbolTable
import TokenTable

class Assembler:
    def __init__(self, instFile):
        self.section = 999
        self.instTable = InstTable.InstTable(instFile)
        self.codeList = []
        self.symtabList = []
        self.literalList = []
        self.tokenList = []
        self.lineList = []

    def loadInputFile(self, inputFile): # inputFile 불러오기
        f = open(inputFile, 'r')
        lines = f.readlines()
        for line in lines:
            self.lineList.append(line) # lineList에 한 line 씩 추가

    def printObjectCode(self,fileName): # Object Program 출력
        f = open(fileName, 'w')
        f.writelines(self.codeList)


    def pass1(self): # input.txt로 만든 lineList를 불러와서 section별로 나눠 토큰 파싱하기
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

    # 분석된 내용을 바탕으로 object code를 생성하여 codeList에 저장
    def pass2(self): # TokenTable.makeObjectCode를 통해 object program 작성
        self.output = ""
        self.H_code = ""
        self.T_code = ""
        self.M_code = ""
        self.E_code = ""
        self.lit_code = ""
        self.loc = ""
        self.leng = 0
        self.total_leng = 0
        self.count = 0 # modification code 작성 시 0의 개수 세는 변수



        ### 섹션별로 토큰테이블 가져오기 ###
        for i in self.tokenList:
            for j in range(len(i.tokenList)):
                t = i.getToken(j)
                i.makeObjectCode(t)

                ### Header 부분 처리 ###
                if t.operator == "START" or t.operator == "CSECT":
                    self.H_code = "H" + t.label + "\t" + str.format("%06X" % (t.location))

                    if t.operator == "START": # START
                        self.loc = str.format("%06X" % (i.getToken(-2).location))
                        self.E_code = "E"+  str.format("%06X" % (t.location))+"\n\n"

                    else:                     # CSECT
                        self.loc = str.format("%06X" % (i.locctr))
                        self.E_code = "E"+"\n\n"
                    self.H_code += self.loc

                elif t.operator == "EXTDEF": # EXTDEF
                    self.H_code += "\nD"
                    for a in range(len(t.operand)):
                        self.loc = str.format("%06X" % (i.symtab.search(t.operand[a])))
                        self.H_code += t.operand[a] + self.loc

                elif t.operator == "EXTREF":   # EXTREF
                    self.H_code += "\nR"
                    for a in range(len(t.operand)):
                        self.H_code += t.operand[a]
                    self.H_code += "\n"

                ### Modification 처리 ###
                elif "+" in t.operator: # 4 형식 M
                    self.loc = str.format("%06X" %(t.location+1))
                    self.count = t.objectCode.count('0')
                    if len(t.operand) == 2:
                        t.operand = t.operand[0]
                    self.M_code += "M" + self.loc + str.format("%02X" %(self.count)) + "+" + t.operand + "\n"

                elif t.operator == "WORD": # WORD M
                    self.loc = str.format("%06X" %(t.location))
                    self.count = t.objectCode.count('0')
                    t.operand = t.operand.split("-")
                    self.M_code += "M" + self.loc + str.format("%02X" %(self.count)) + "+" + t.operand[0]+"\n"
                    self.M_code += "M" + self.loc + str.format("%02X" %(self.count)) + "-" + t.operand[0]+"\n"

                ### Text 부분 처리 ###
                elif t.location == 0 and t.objectCode != "" :
                    self.loc = str.format("%06X" %(t.location))
                    self.output += "T"+self.loc
                    for m in range(len(i.tokenList)):
                        tt = i.getToken(m)
                        i.makeObjectCode(tt)
                        self.leng = tt.byteSize

                        if self.total_leng + self.leng > 30: ## T 라인 길이 재기
                            self.output += str.format("%02X" %(self.total_leng)) + self.T_code
                            self.total_leng = 0
                            self.loc = str.format("%06X" %(tt.location))
                            self.output += "\nT"+self.loc
                            self.T_code = ""
                        self.total_leng += self.leng
                        self.T_code += tt.objectCode
                    self.output += str.format("%02X" %(self.total_leng)) + self.T_code +"\n"

                elif "=" in t.operand: # 리터럴 처리 부분
                    for a in range(len(i.tokenList)):
                        if i.littab.search(t.operand) != -1:
                            self.litloc = i.littab.search(t.operand) # 리터럴 값 적힐 주소 가져오기
                            break
                    for b in range(len(i.tokenList)):
                        if self.litloc == i.getToken(b).location and self.litloc != 0:
                            if "=C" in t.operand: # 문자열 literal 처리
                                self.lit_code += "T" + str.format("%06X" %self.litloc)+str.format("%02X" %t.litSize)+t.literal+"\n"


            print(self.H_code+self.output+self.lit_code+self.M_code+self.E_code)

            self.codeList.append(self.H_code+self.output+self.lit_code+self.M_code+self.E_code) # 정리한 object code codeList에 추가


            ## codeList에 추가해준 code 들을 초기화 해줌 ##

            self.output = ""
            self.M_code = ""
            self.T_code = ""
            self.total_leng = 0
            self.litloc = ""
            self.lit_code = ""
            self.E_code = ""

if __name__ == '__main__': # main 루틴

    assembler = Assembler("inst.data")
    assembler.loadInputFile("input.txt")
    assembler.pass1()
    assembler.pass2();
    assembler.printObjectCode("output_20160273.txt");