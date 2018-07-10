class SymbolTable:

    def __init__(self):
        self.symbolList = []
        self.locationList = []
        self.literalList = []
 #       self.Symbol = []
    def putSymbol(self, symbol, location):
        self.symbolList.append(symbol)
        self.locationList.append(location)
  #      self.Symbol.append(symbol,location)

    def modifySymbol(self, symbol, newLocation):
        if self.search(symbol)!= -1:
            self.literalList.append(symbol.split("'")[0])
            for i in self.symbolList:
                if symbol==i:
                    n = self.symbolList.index(symbol)
                    self.locationList[n] = newLocation
        else:
            self.putSymbol(symbol, newLocation)
    def search(self, symbol):
        address = 0
        if symbol in self.symbolList:
            n = self.symbolList.index(symbol)
            address = self.locationList[n]
        else:
            return -1
        return address