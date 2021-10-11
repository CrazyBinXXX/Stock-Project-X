class Strategy():
    def __init__(self):
        self.name = ''
        self.type = ''
        self.account = None
        self.ticker = 'QQQ'
        self.lastDate = None
        self.simulator = None

    def seeDate(self):
        return self.account.seeDate()

    def seePrice(self, ticker):
        return self.account.seePrice()

    def step(self):
        pass