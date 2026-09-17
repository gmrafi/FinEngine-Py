"""Core deterministic financial math and precision primitives.

All functions in this module are 100% zero-dependency pure Python.
"""

from .amortization import AmortizationPlan, AmortizationRow, amortize, monthly_payment
from .money import Money, SupportedCurrency, create_money, format_money, round2, round4
from .xirr import CashFlow, xirr

__all__ = [
    "Money",
    "SupportedCurrency",
    "create_money",
    "format_money",
    "round2",
    "round4",
    "AmortizationRow",
    "AmortizationPlan",
    "monthly_payment",
    "amortize",
    "CashFlow",
    "xirr",
]
