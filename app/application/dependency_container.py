"""
============================================================

                    STACKED ONE

              DEPENDENCY CONTAINER

------------------------------------------------------------

Central registry for singleton services.

============================================================
"""

from __future__ import annotations


class DependencyContainer:
    """
    Very lightweight dependency injection container.
    """

    # =====================================================

    def __init__(self):

        self._services: dict[str, object] = {}

    # =====================================================

    def register(

        self,

        name: str,

        service: object,

    ) -> None:

        if name in self._services:

            raise ValueError(

                f"Service '{name}' already registered."

            )

        self._services[name] = service

    # =====================================================

    def resolve(

        self,

        name: str,

    ) -> object:

        if name not in self._services:

            raise KeyError(

                f"Service '{name}' not found."

            )

        return self._services[name]

    # =====================================================

    def contains(

        self,

        name: str,

    ) -> bool:

        return name in self._services

    # =====================================================

    def clear(self):

        self._services.clear()

    # =====================================================

    @property
    def services(self):

        return tuple(

            self._services.keys()

        )

    # =====================================================

    def __len__(self):

        return len(

            self._services,

        )

    # =====================================================

    def __str__(self):

        return (

            "DependencyContainer("

            f"{len(self)} services"

            ")"

        )

    __repr__ = __str__