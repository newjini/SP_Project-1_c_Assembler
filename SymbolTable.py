
class SymbolTable: ## symbol과 관련된 데이터,연산 관리

    def __init__(self,section):
        self.symbolList = []
        self.locationList = []
        self.literalList = [] ## literal 처리 시에 사용하는 list
        self.section = section

    ### 새로운 symbol을 table에 추가
    ### symbol : 새로 추가되는 symbol의 label
    ### location : 해당 symbol이 가지는 주소값

    def putSymbol(self, symbol, location):
        self.symbolList.append(symbol)
        self.locationList.append(location)

    ### 기존에 존재하는 symbol 값에 대해서 가리키는 주소값을 변경하는데
    ### 이 때 symbol이 symbolList에 존재하지 않는다면 putSymbol로 symbolList에 추가해줌
    def modifySymbol(self, symbol, newLocation):
        if self.search(symbol)!= -1:
            self.literalList.append(symbol.split("'")[0])
            for i in self.symbolList:
                if symbol==i:
                    n = self.symbolList.index(symbol)
                    self.locationList[n] = newLocation
        else:
            self.putSymbol(symbol, newLocation)
    ### 인자로 전달된 symbol이 어떤 주소를 지칭하는지 알려줌 ###
    ### return 값 : symbol이 가지고 있는 주소값. 해당 symbol이 없을 경우 -1 리턴
    def search(self, symbol):
        self.address = 0
        if symbol in self.symbolList: ## 심볼테이블에 현재 symbol이 존재한다면
            n = self.symbolList.index(symbol)
            self.address = self.locationList[n] ## 해당하는 주소 리턴
        else:
            return -1
        return self.address
