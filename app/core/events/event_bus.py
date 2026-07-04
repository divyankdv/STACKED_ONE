"""
============================================================

                    STACKED ONE

                    EVENT BUS

------------------------------------------------------------

Central event dispatcher for the entire STACKED ONE
platform.

Supports:

    • Thread-safe publish
    • Multiple subscribers
    • Event history
    • Statistics
    • Subscriber isolation

============================================================
"""

from __future__ import annotations

from collections import defaultdict, deque
from threading import RLock

from app.core.events.event import Event
from app.core.events.event_types import EventType
from app.core.events.subscriber import Subscriber


class EventBus:

    """
    Central event dispatcher.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(

        self,

        history_size: int = 1000,

    ):

        self._subscribers: dict[
            EventType,
            list[Subscriber],
        ] = defaultdict(list)

        self._history: deque[Event] = deque(

            maxlen=history_size,

        )

        self._publish_count = 0

        self._lock = RLock()

    # =====================================================
    # Subscribe
    # =====================================================

    def subscribe(

        self,

        event_type: EventType,

        subscriber: Subscriber,

    ) -> None:

        with self._lock:

            subscribers = self._subscribers[event_type]

            if subscriber not in subscribers:

                subscribers.append(

                    subscriber,

                )

    # =====================================================
    # Unsubscribe
    # =====================================================

    def unsubscribe(

        self,

        event_type: EventType,

        subscriber: Subscriber,

    ) -> None:

        with self._lock:

            subscribers = self._subscribers.get(

                event_type,

            )

            if not subscribers:

                return

            if subscriber in subscribers:

                subscribers.remove(

                    subscriber,

                )

    # =====================================================
    # Publish
    # =====================================================

    def publish(

        self,

        event: Event,

    ) -> None:

        #
        # Copy subscribers while locked
        #

        with self._lock:

            self._publish_count += 1

            self._history.append(

                event,

            )

            subscribers = tuple(

                self._subscribers.get(

                    event.event_type,

                    (),

                )

            )

        #
        # Notify outside the lock
        #

        for subscriber in subscribers:

            try:

                subscriber.on_event(

                    event,

                )

            except Exception as exc:

                #
                # Never allow one subscriber
                # to stop the bus.
                #

                print(

                    f"[EVENT BUS] "

                    f"{subscriber.name} "

                    f"failed: {exc}"

                )

    # =====================================================
    # Clear
    # =====================================================

    def clear(self):

        with self._lock:

            self._subscribers.clear()

            self._history.clear()

            self._publish_count = 0

    # =====================================================
    # History
    # =====================================================

    @property
    def history(self):

        return tuple(

            self._history,

        )

    @property
    def history_size(self):

        return len(

            self._history,

        )

    # =====================================================
    # Statistics
    # =====================================================

    @property
    def publish_count(self):

        return self._publish_count

    @property
    def subscriber_count(self):

        return sum(

            len(subscribers)

            for subscribers

            in self._subscribers.values()

        )

    @property
    def event_types(self):

        return tuple(

            self._subscribers.keys()

        )

    # =====================================================
    # Lookup
    # =====================================================

    def subscribers(

        self,

        event_type: EventType,

    ) -> tuple[Subscriber, ...]:

        return tuple(

            self._subscribers.get(

                event_type,

                (),

            )

        )

    # =====================================================
    # Contains
    # =====================================================

    def has_subscribers(

        self,

        event_type: EventType,

    ) -> bool:

        return (

            len(

                self._subscribers.get(

                    event_type,

                    (),

                )

            )

            > 0

        )

    # =====================================================
    # String
    # =====================================================

    def __len__(self):

        return self.subscriber_count

    def __str__(self):

        return (

            "EventBus("

            f"events={self.publish_count}, "

            f"subscribers={self.subscriber_count}, "

            f"history={self.history_size}"

            ")"

        )

    __repr__ = __str__