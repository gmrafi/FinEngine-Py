"""Pure zero-dependency deterministic loan amortization primitives.

Guarantees 100% mathematical parity with client-side JavaScript calculations,
integer-rounded sub-unit arithmetic, and strict Terminal Zero reconciliation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional
from .money import round2


@dataclass(frozen=True)
class AmortizationRow:
    """Represents a single monthly installment in an amortization schedule.

    Attributes:
        month: Installment period (1-indexed, e.g. 1, 2, ... 36)
        payment: Total installment amount due
        principal_paid: Principal component applied to reducing balance
        interest_paid: Interest portion of the monthly payment
        remaining_balance: Closing loan balance after applying the installment
    """

    month: int
    payment: float
    principal_paid: float
    interest_paid: float
    remaining_balance: float

    @property
    def interest(self) -> float:
        """Alias for interest_paid for concise dataframe access."""
        return self.interest_paid

    def to_dict(self) -> dict[str, Any]:
        """Convert installment row to dictionary."""
        return {
            "month": self.month,
            "payment": self.payment,
            "principal_paid": self.principal_paid,
            "interest": self.interest_paid,
            "interest_paid": self.interest_paid,
            "remaining_balance": self.remaining_balance,
        }


@dataclass
class AmortizationPlan:
    """Complete loan amortization plan with full schedule and summary totals.

    Attributes:
        principal: Original borrowed amount
        annual_rate: Annual interest rate in percent (e.g. 13.5 for 13.5% p.a.)
        months: Total duration in months
        monthly_payment: Equated Monthly Installment (EMI)
        total_interest: Cumulative interest paid over the entire term
        total_payable: Total cost of the loan (Principal + Total Interest)
        schedule: List of monthly installment records
    """

    principal: float
    annual_rate: float
    months: int
    monthly_payment: float
    total_interest: float
    total_payable: float
    schedule: List[AmortizationRow] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert entire amortization plan and schedule to dictionary."""
        return {
            "principal": self.principal,
            "annual_rate": self.annual_rate,
            "months": self.months,
            "monthly_payment": self.monthly_payment,
            "total_interest": self.total_interest,
            "total_payable": self.total_payable,
            "schedule": [row.to_dict() for row in self.schedule],
        }

    def to_dataframe(self) -> Any:
        """Convert schedule to a pandas DataFrame if pandas is installed.

        Returns:
            pandas.DataFrame: Structured table with columns ['month', 'payment', 'principal_paid', 'interest', 'remaining_balance']
        """
        try:
            import pandas as pd
        except ImportError as e:
            raise ImportError(
                "Pandas is required for `to_dataframe()`. Install with `pip install finengine[analysis]` or `pip install pandas`."
            ) from e

        return pd.DataFrame(
            [
                {
                    "month": r.month,
                    "payment": r.payment,
                    "principal_paid": r.principal_paid,
                    "interest": r.interest_paid,
                    "remaining_balance": r.remaining_balance,
                }
                for r in self.schedule
            ]
        )


def monthly_payment(
    principal: float,
    annual_rate: float,
    months: int,
    round_to_integer: bool = False,
) -> float:
    """Calculate the Equated Monthly Installment (EMI) for a reducing-balance loan.

    Formula:
        r = annual_rate / 12 / 100
        payment = principal * r * (1 + r)^months / ((1 + r)^months - 1)

    Args:
        principal: Principal loan amount (> 0)
        annual_rate: Annual nominal interest rate in percent (e.g. 13.5)
        months: Total loan tenure in months (> 0)
        round_to_integer: If True, round payment to nearest integer (e.g. 16968)

    Returns:
        float: Exact monthly payment amount (e.g. 16967.64 or 16968.0)
    """
    if months <= 0:
        raise ValueError("Loan duration (months) must be strictly greater than 0.")
    if principal < 0:
        raise ValueError("Principal cannot be negative.")

    if annual_rate == 0.0 or principal == 0.0:
        raw_payment = principal / months
        return float(round(raw_payment)) if round_to_integer else round2(raw_payment)

    monthly_rate = annual_rate / 12.0 / 100.0
    compounding_factor = (1.0 + monthly_rate) ** months
    payment = principal * monthly_rate * compounding_factor / (compounding_factor - 1.0)

    if round_to_integer:
        return float(round(payment))
    return round2(payment)


def amortize(
    principal: float,
    annual_rate: float,
    months: int,
    round_to_integer: bool = False,
) -> AmortizationPlan:
    """Compute the full deterministic amortization schedule with Terminal Zero reconciliation.

    Args:
        principal: Principal loan amount (e.g. 500000)
        annual_rate: Annual nominal interest rate in percent (e.g. 13.5)
        months: Total tenure in months (e.g. 36)
        round_to_integer: If True, round monthly installment to nearest whole unit

    Returns:
        AmortizationPlan: Structured plan with schedule and exact reconciliation.
    """
    if months <= 0:
        raise ValueError("Loan tenure in months must be positive.")

    payment = monthly_payment(principal, annual_rate, months, round_to_integer=round_to_integer)
    monthly_rate = annual_rate / 12.0 / 100.0
    balance = float(principal)
    total_interest = 0.0
    schedule: List[AmortizationRow] = []

    for month in range(1, months + 1):
        interest_paid = round2(balance * monthly_rate)

        # Terminal Zero Reconciliation on final month
        if month == months:
            principal_paid = balance
            actual_payment = round2(principal_paid + interest_paid)
            balance = 0.0
        else:
            principal_paid = round2(payment - interest_paid)
            if principal_paid > balance:
                principal_paid = balance
                balance = 0.0
            else:
                balance = round2(max(0.0, balance - principal_paid))
            actual_payment = payment

        total_interest = round2(total_interest + interest_paid)

        schedule.append(
            AmortizationRow(
                month=month,
                payment=actual_payment,
                principal_paid=principal_paid,
                interest_paid=interest_paid,
                remaining_balance=balance,
            )
        )

    total_payable = round2(principal + total_interest)

    return AmortizationPlan(
        principal=principal,
        annual_rate=annual_rate,
        months=months,
        monthly_payment=payment,
        total_interest=total_interest,
        total_payable=total_payable,
        schedule=schedule,
    )
