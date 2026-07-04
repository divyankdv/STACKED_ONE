"""
============================================================

                    STACKED ONE

                    BOOTSTRAP

============================================================
"""

from __future__ import annotations

from app.application.container_builder import ContainerBuilder


class Bootstrap:

    @staticmethod
    def build():

        return ContainerBuilder().build()