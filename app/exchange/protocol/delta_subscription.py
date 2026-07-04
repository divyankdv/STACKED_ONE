from dataclasses import dataclass

from app.exchange.protocol.delta_channels import DeltaChannel


@dataclass(slots=True)
class DeltaSubscription:

    channel: DeltaChannel

    symbols: list[str]

    def to_dict(self):

        return {

            "name": self.channel.value,

            "symbols": self.symbols,

        }