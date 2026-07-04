from enum import Enum


class SignalSide(str, Enum):

    BUY = "BUY"

    SELL = "SELL"

    NEUTRAL = "NEUTRAL"