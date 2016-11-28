from datetime import datetime

from pony.orm import Database, PrimaryKey, Required, Optional, Json

db = Database()


class Transfer(db.Entity):
    _table_ = 'Transfers'
    id = PrimaryKey(int, auto=True)

    _from = Required(str)
    to = Required(str)
    amount = Required(float)
    currency = Required(str)
    memo = Optional(str)

    timestamp = Optional(datetime)
    block_id = Optional(int)
    meta = Optional(Json)


class Account(db.Entity):
    _table_ = 'Accounts'
    id = PrimaryKey(int, auto=True)

    name = Required(str)
    info = Required(Json)

    sp = Optional(float)
    rep = Optional(float)

