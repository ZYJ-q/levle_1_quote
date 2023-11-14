from datatypes import *
from redpanda_publisher import RedpandaPublisher, dataclass_to_dict
from market_data import Level1Snapshot


class Level1SnapshotPublisher(RedpandaPublisher):
    def __init__(self):
        super().__init__("level_1_quote.avsc", dataclass_to_dict, "level_1_quotes")


if __name__ == "__main__":
    import time
    import random

    symbol = "TEST.SYM"
    exchange = "TEST.EXCH"

    publisher = Level1SnapshotPublisher()
    for i in range(10):
        receive_time = int(time.time() * 1000)
        exchange_time = receive_time - 100
        bid = random.randint(100, 105)
        bid_qty = random.randint(1, 10)
        ask = random.randint(bid + 1, bid + 5)
        bid *= 1_000_000
        ask *= 1_000_000
        ask_qty = random.randint(1, 10)
        snapshot = Level1Snapshot(
            symbol, exchange, receive_time, exchange_time, bid, bid_qty, ask, ask_qty
        )
        publisher.add_record(snapshot)
        time.sleep(1)
