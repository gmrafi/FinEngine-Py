"""FinEngine Python SDK - Deterministic Financial Math & Quantitative Primitives.

A CFSBR Computational Initiative.
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

__version__ = "0.1.0"
__author__ = "CFSBR Computational Team"

__all__ = [
    "__version__",
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
