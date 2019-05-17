import time
from random import randint
from app.orm import ORM
from app.util import hash_pass, get_price
from app.position import Position
from app.trade import Trade

class Account(ORM):
    fields = ["username", "password_hash", "balance", "api_key"]
    table = "accounts"

    def __init__(self):
        self.pk = None
        self.username = None
        self.password_hash = None
        self.balance = None
        self.api_key = randint(100000000000000, 999999999999999)

    def set_password(self, password):
        self.password_hash = hash_pass(password)

    @classmethod
    def api_authenticate(cls, api_key):
        account = cls.select_one("WHERE api_key = ?", (api_key, ))
        if not account:
            return None
        else:
            return account

    @classmethod
    def login(cls, username, password):
        account = cls.select_one("WHERE password_hash = ? AND username = ?", (hash_pass(password), username))
        if not account:
            return None
        else:
            return account

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("cannot make negative deposit")
        self.balance += amount
        self.save()
        return self.balance

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("cannot make negative withdrawl")
        self.balance -= amount
        self.save()
        return self.balance

    def get_positions(self):
        """ return a list of each Position object for this user """
        where = "WHERE account_pk = ?"
        values = (self.pk, )
        return Position.select_many(where, values)

    def get_trades(self):
        """ return a list of all Trades for this user """
        where = "WHERE account_pk = ?"
        values = (self.pk, )
        return Trade.select_many(where, values)
    
    def get_trades_orderby(self):
        """ return a list of all Trades for this user """
        where = "WHERE account_pk = ?"
        order = "ORDER BY time DESC"
        values = (self.pk, )
        return Trade.select_many_orderby(where, order, values)

    def get_trades_for(self, symbol):
        """ return a list of all Trades for a given symbol for this user """
        where = "WHERE account_pk = ? AND ticker = ?"
        values = (self.pk, symbol)
        return Trade.select_many(where, values)

    def get_position_for(self, ticker):
        where = "WHERE account_pk = ? AND ticker = ?"
        values = (self.pk, ticker)
        result = Position.select_one(where, values)
        if result:
            return result

        position = Position()
        position.account_pk = self.pk
        position.ticker = ticker
        position.shares = 0
        return position

    def buy(self, ticker, amount):
        price = get_price(ticker)
        if self.balance < price * amount:
            raise ValueError("Insufficient Funds")
        self.balance -= price * amount
        trade = Trade()
        trade.account_pk = self.pk
        trade.ticker = ticker
        trade.price = price
        trade.volume = amount
        trade.time = time.time()

        position = self.get_position_for(ticker)
        position.shares += amount
        self.save()
        trade.save()
        position.save()

    def sell(self, ticker, amount):
        price = get_price(ticker)
        position = self.get_position_for(ticker)
        if position.shares < amount:
            raise ValueError(
                "Insufficient Shares to Sell or Position Does not Exist")
        self.balance += price * amount
        trade = Trade()
        trade.account_pk = self.pk
        trade.ticker = ticker
        trade.price = price
        trade.volume = -1 * amount
        trade.time = time.time()

        position.shares -= amount
        self.save()
        trade.save()
        position.save()
