"""FinEngine Python SDK - Deterministic Financial Math & Quantitative Primitives.

Developed by Md Golam Mubasshir Rafi.
A computational research initiative by the Centre for Fintech & Strategic Business Research (CFSBR).
"""

from __future__ import annotations

from finengine.ai import (
    CreditAssessment,
    CreditScorer,
    MFSProfile,
    assess_credit_risk,
)
from finengine.analytics import (
    Prepayment,
    batch_amortize,
    portfolio_summary,
    simulate_loan,
    to_dataframe,
)
from finengine.math import (
    AmortizationPlan,
    AmortizationRow,
    CashFlow,
    Money,
    SupportedCurrency,
    amortize,
    create_money,
    format_money,
    monthly_payment,
    round2,
    round4,
    xirr,
)

__version__ = "0.1.1"
__author__ = "Md Golam Mubasshir Rafi"
__email__ = "rafi@gmrafi.com.bd"
__affiliation__ = "Centre for Fintech & Strategic Business Research (CFSBR)"

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__affiliation__",
    "amortize",
    "monthly_payment",
    "xirr",
    "CashFlow",
    "Money",
    "SupportedCurrency",
    "create_money",
    "format_money",
    "round2",
    "round4",
    "AmortizationPlan",
    "AmortizationRow",
    "to_dataframe",
    "batch_amortize",
    "portfolio_summary",
    "simulate_loan",
    "Prepayment",
    "CreditScorer",
    "CreditAssessment",
    "MFSProfile",
    "assess_credit_risk",
]
