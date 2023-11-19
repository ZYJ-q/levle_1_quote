from datatypes import *
from redpanda_publisher import RedpandaPublisher
import market_data_pb2 as md


class Level1SnapshotPublisher(RedpandaPublisher):
    def __init__(self):
        super().__init__(md.Quotes, "quotes")


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
        snapshot = md.Quotes(
            symbol=symbol,
            exchange=exchange,
            receive_time=receive_time,
            exchange_time=exchange_time,
            bid=bid,
            bid_qty=bid_qty,
            ask=ask,
            ask_qty=ask_qty,
        )
        publisher.add_record(snapshot)
        time.sleep(1)
