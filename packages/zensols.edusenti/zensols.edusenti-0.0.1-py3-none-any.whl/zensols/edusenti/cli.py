"""Command line entry point to the application.

"""
__author__ = 'Paul Landes'

from typing import List, Any, Type, Dict
import sys
from zensols.cli import ActionResult, CliHarness
from zensols.cli import ApplicationFactory as CliApplicationFactory
from .app import Application


class ApplicationFactory(CliApplicationFactory):
    def __init__(self, *args, **kwargs):
        kwargs['package_resource'] = 'zensols.edusenti'
        super().__init__(*args, **kwargs)

    @classmethod
    def get_application(cls: Type) -> Application:
        """Get the prediction app with the ``predict`` method."""
        harness: CliHarness = cls.create_harness()
        return harness.get_application()


def main(args: List[str] = sys.argv, **kwargs: Dict[str, Any]) -> ActionResult:
    harness: CliHarness = ApplicationFactory.create_harness(relocate=False)
    harness.invoke(args, **kwargs)
