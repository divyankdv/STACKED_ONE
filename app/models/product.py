"""
============================================================

                STACKED QUANT AI V6

                PRODUCT MODEL

------------------------------------------------------------

Represents an exchange trading instrument.

Every engine should use this object instead of
raw JSON from the exchange.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Product:

    # -----------------------------------------------------
    # Identity
    # -----------------------------------------------------

    id: int

    symbol: str

    description: str

    contract_type: str

    state: str

    trading_status: str

    # -----------------------------------------------------
    # Pricing
    # -----------------------------------------------------

    tick_size: float

    contract_value: float

    impact_size: float

    # -----------------------------------------------------
    # Margin
    # -----------------------------------------------------

    default_leverage: float

    initial_margin: float

    maintenance_margin: float

    max_leverage_notional: float

    # -----------------------------------------------------
    # Fees
    # -----------------------------------------------------

    maker_fee: float

    taker_fee: float

    annualized_funding: float

    # -----------------------------------------------------
    # Assets
    # -----------------------------------------------------

    underlying: str

    quote: str

    settlement: str

    # =====================================================
    # Constructors
    # =====================================================

    @classmethod
    def from_delta(
        cls,
        data: dict[str, Any],
    ) -> Product:

        quoting = data.get("quoting_asset", {})
        settling = data.get("settling_asset", {})
        underlying = data.get("underlying_asset", {})

        return cls(

            id=int(data["id"]),

            symbol=data["symbol"],

            description=data.get("description", ""),

            contract_type=data.get("contract_type", ""),

            state=data.get("state", ""),

            trading_status=data.get("trading_status", ""),

            tick_size=float(data.get("tick_size", 0)),

            contract_value=float(
                data.get("contract_value", 0)
            ),

            impact_size=float(
                data.get("impact_size", 0)
            ),

            default_leverage=float(
                data.get("default_leverage", 0)
            ),

            initial_margin=float(
                data.get("initial_margin", 0)
            ),

            maintenance_margin=float(
                data.get("maintenance_margin", 0)
            ),

            max_leverage_notional=float(
                data.get(
                    "max_leverage_notional",
                    0,
                )
            ),

            maker_fee=float(
                data.get(
                    "maker_commission_rate",
                    0,
                )
            ),

            taker_fee=float(
                data.get(
                    "taker_commission_rate",
                    0,
                )
            ),

            annualized_funding=float(
                data.get(
                    "annualized_funding",
                    0,
                )
            ),

            underlying=underlying.get(
                "symbol",
                "",
            ),

            quote=quoting.get(
                "symbol",
                "",
            ),

            settlement=settling.get(
                "symbol",
                "",
            ),

        )

    # =====================================================
    # Convenience
    # =====================================================

    @property
    def is_live(self) -> bool:

        return self.state.lower() == "live"

    @property
    def is_perpetual(self) -> bool:

        return self.contract_type == "perpetual_futures"

    def __str__(self) -> str:

        return (

            f"{self.symbol} | "

            f"ID={self.id} | "

            f"Tick={self.tick_size} | "

            f"Leverage={self.default_leverage}x"

        )