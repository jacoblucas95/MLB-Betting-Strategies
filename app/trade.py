from app import util
from app.orm import ORM

class Trade(ORM):
    fields = ['account_pk', 'ticker', 'volume', 'price', 'time'] 
    table = 'trades'

    def __init__(self):
        self.pk = None
        self.account_pk = None
        self.ticker = None
        self.volume = None
        self.price = None
        self.time = None

    def json(self):
        return {"ticker": self.ticker, "volume": self.volume, "price": self.price, "time": self.time}
