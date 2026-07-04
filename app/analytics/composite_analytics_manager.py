"""
============================================================

                    STACKED ONE

          COMPOSITE ANALYTICS MANAGER

------------------------------------------------------------

Executes all Composite Analytics Engines.

Responsibilities
----------------
✓ Build CompositeAnalyticsContext
✓ Execute every composite engine
✓ Validate dependencies
✓ Store snapshots back into the context

============================================================
"""

from __future__ import annotations

from app.analytics.composite_context import CompositeAnalyticsContext
from app.analytics.composite_engine_registry import (
    COMPOSITE_ENGINE_REGISTRY,
)


class CompositeAnalyticsManager:

    """
    Executes all composite analytics engines.

    Composite engines consume CompositeAnalyticsContext
    and enrich it with higher-level analytics.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self.engines = []

        for engine_cls in COMPOSITE_ENGINE_REGISTRY:

            self.register(

                engine_cls()

            )

    # =====================================================
    # Register Engine
    # =====================================================

    def register(

        self,

        engine,

    ):

        if not hasattr(engine, "snapshot_name"):

            raise TypeError(

                f"{engine.__class__.__name__} "

                "does not define snapshot_name."

            )

        if not hasattr(engine, "dependencies"):

            raise TypeError(

                f"{engine.__class__.__name__} "

                "does not define dependencies."

            )

        self.engines.append(

            engine

        )

    # =====================================================
    # Update
    # =====================================================

    def update(

        self,

        analytics_snapshot,

    ) -> CompositeAnalyticsContext:

        #
        # Create fresh context
        #

        context = CompositeAnalyticsContext(

            analytics=analytics_snapshot

        )

        #
        # Execute every engine
        #

        for engine in self.engines:

            #
            # Validate dependencies
            #

            for dependency in engine.dependencies:

                if getattr(

                    context,

                    dependency,

                    None,

                ) is None:

                    raise RuntimeError(

                        f"{engine.snapshot_name} "

                        f"requires "

                        f"'{dependency}' "

                        f"before execution."

                    )

            #
            # Execute engine
            #

            engine.update(

                context

            )

            #
            # Store snapshot
            #

            setattr(

                context,

                engine.snapshot_name,

                engine.snapshot(),

            )

        return context

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        for engine in self.engines:

            engine.reset()

    # =====================================================
    # Number of Engines
    # =====================================================

    @property
    def engine_count(self):

        return len(

            self.engines

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        names = [

            engine.snapshot_name

            for engine in self.engines

        ]

        return (

            f"CompositeAnalyticsManager("

            f"engines={names})"

        )

    __repr__ = __str__