
class InstTable: ## 모든 instruction 정보 관리 클래스, instruction data를 저장함

    def __init__(self, fileName):
        self.instDic = {}
        self.openFile(fileName)

    ### inst.data 파일을 불러와 저장하는 공간
    ### instDic 을 통해 명령어의 이름을 넣으면 instruction 정보 리턴 가능
    def openFile(self, fileName):
        file = open(fileName, 'r')
        lines = file.readlines( )
        for line in lines:
            inst = Instruction(line)
            self.instDic[inst.instruction] = inst
        file.close( )


class Instruction: ## 명령어 하나하나의 구체적인 정보는 Instruction클래스에 담음
    def __init__(self, line): ## instruction과 관련된 정보들을 저장하고 기초적인 연산을 수행

        self.i_token = None
        self.instruction = ""
        self.opcode = 0
        self.numberOfoperand = 0
        self.format = None ## instruction이 몇 바이트 명령어인지 저장.

        self.parsing(line)

    ### 클래스를 선언하면서 일반문자열을 즉시 구조에 맞게 파싱함 ###
    def parsing(self, line):
        i_token = line.split( )
        self.instruction = i_token[0]

        if i_token[1] == "3/4": ## 형식이 3/4일 때, 3으로 변경해줌
            self.format = 3
        else:
            self.format = i_token[1]
        self.opcode = (int(i_token[2],16)) ## opcode 는 16진수로 사용
        self.numberOfoperand = i_token[3]