from dataclasses import dataclass
from datatypes import *


@dataclass
class Level1Snapshot:
    symbol: SymbolId = ""
    exchange: ExchangeId = ""
    receive_time: Timestamp = 0
    exchange_time: Timestamp = 0
    bid: Price = 0
    bid_qty: Quantity = 0
    ask: Price = 0
    ask_qty: Quantity = 0
