"""
============================================================

                STACKED QUANT AI V6

                BASE ENGINE

Every engine inherits from this class.

============================================================
"""


class BaseEngine:

    def initialize(self):
        """
        Called once during startup.
        """
        pass

    def update(self, *args, **kwargs):
        """
        Called whenever new market data arrives.
        """
        pass

    def reset(self):
        """
        Reset engine state.
        """
        pass