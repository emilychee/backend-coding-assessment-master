"""Check Python style with pycodestyle and pydocstyle."""

import pytest
import requests
import os
import sh
import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from review_analysis import *

class TestPythonStyle():
    """Unit tests for Python code style."""

    def test_pydocstyle(self):
        """Run `pydocstyle review_analysis.py`."""
        pydocstyle = sh.Command("pydocstyle")
        output = pydocstyle("review_analysis.py")
        assert(output.exit_code == 0)

    def test_pycodestyle(self):
        """Run `pycodestyle on review_analysis.py`."""
        output = sh.pycodestyle("review_analysis.py")
        assert(output.exit_code == 0)