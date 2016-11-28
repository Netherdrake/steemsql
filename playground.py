from random import shuffle

from pony.orm import db_session, commit, select
from steemtools import base
from steemtools.blockchain import Blockchain
from tqdm import tqdm

from models import *

# initialize the db
db.bind('sqlite', ':memory:', create_db=True)
db.generate_mapping(create_tables=True)


@db_session
def scrape_users():
    b = Blockchain()
    users = b.get_all_usernames()
    shuffle(users)

    for username in tqdm(users[:100]):
        a = base.Account(username)
        # pprint(a.get_props())
        Account(
            name=username, info=a.get_props(),
            sp=a.sp, rep=a.rep,
        )
        commit()

    # in our 100 user random sample, find 10 accounts with more than 20 SP that have NOT been mined
    select(p for p in Account if p.sp > 20 and p.info['mined'] is False).limit(10).show()


if __name__ == '__main__':
    scrape_users()
