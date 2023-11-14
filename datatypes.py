from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Type, Union
from dataclasses import dataclass

import numpy as np

JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]

Timestamp = int
ClientOrderId = int
MetaOrderId = int
ChildOrderId = int
ExchangeOrderId = int
InstructionId = int
ClientId = int
AccountId = int
Quantity = int
SymbolId = str
ExchangeId = str


@dataclass
class Symbol:
    sym: str
    tick_size: int
    lot_size: int


class Direction(Enum):
    Bid = 1
    Ask = -1


OrderStatus = Enum(
    "OrderStatus",
    ["NACK", "SENDING", "ACK", "STARTED", "REJ", "PARTIAL_FILL", "COMPLETED"],
)
Offset = Enum("Offset", ["Open", "Close", "CloseToday", "CloseYesterday", "Undefined"])

AlgoType = Enum("AlgoType", ["TWAP", "VWAP", "Float", "LiqSeeker"])
Price = int
Memo = str
PassThrough = str

SORTactic = str
AdvancedParams = JSON
