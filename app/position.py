from app import util
from app.orm import ORM


class Position(ORM):
    fields = ["account_pk", "ticker", "shares"]
    table = "positions"

    def __init__(self):
        self.pk = None
        self.account_pk = None
        self.ticker = None
        self.shares = None

    def json(self):
        return {"ticker": self.ticker, "shares": self.shares}
