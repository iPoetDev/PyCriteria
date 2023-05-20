#!/user/bin/env python3
# pylint: disable=trailing-whitespace
# ruff: noqa: ANN001, I001
"""Module: PyCriteria: Types"""

from typing import Literal

# VauleTypes: Literals
ActionType = Literal["default", "error", "ignore", "always", "module", "once"]
