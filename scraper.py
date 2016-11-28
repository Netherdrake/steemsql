from pony.orm import commit, select, db_session, desc
from steemtools.blockchain import Blockchain
from steemtools.helpers import read_asset

from helpers import scrape_with_progress
from models import *

# initialize the db
db.bind('sqlite', ':memory:', create_db=True)
db.generate_mapping(create_tables=True)
# sql_debug(True)

b = Blockchain()
print(b.steem.rpc.url)
results = scrape_with_progress(b.get_current_block() - 200, b.get_current_block(), filter_by="transfer")

with db_session:
    for event in results:
        op = event['op']
        asset = read_asset(op['amount'])
        t = Transfer(
            to=op['to'], _from=op['from'],
            amount=asset['value'], currency=asset['symbol'], memo=op['memo'],
            timestamp=event['timestamp'], block_id=event['block_id'],
        )
        commit()

    print("\nTop 10 transfers in last 200 blocks:")
    select(p for p in Transfer if p.amount > 1).order_by(desc(Transfer.amount))[:10].show()

    print("\nAvg SBD transfer size:")
    print(select(p.amount for p in Transfer if p.currency == 'SBD').avg())
