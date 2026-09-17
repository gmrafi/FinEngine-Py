"""Scenario simulations, prepayment acceleration, and default stress-testing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from finengine.math.amortization import monthly_payment
from finengine.math.money import round2


@dataclass
class Prepayment:
    """Represents a scheduled prepayment or extra principal reduction."""

    month: int
    amount: float
    recurring: bool = False


def simulate_loan(
    principal: float,
    annual_rate: float,
    months: int,
    prepayments: Optional[List[Prepayment]] = None,
    default_month: Optional[int] = None,
    recovery_rate: float = 0.0,
) -> Dict[str, Any]:
    """Simulate loan performance under prepayment acceleration or default scenarios.

    Args:
        principal: Principal loan amount
        annual_rate: Annual nominal rate in percent
        months: Original contractual tenure in months
        prepayments: Optional list of Prepayment objects specifying extra principal contributions
        default_month: Month in which borrower defaults and ceases all payments
        recovery_rate: Expected recovery rate on default (0.0 to 1.0)

    Returns:
        Dict[str, Any]: Detailed simulation metrics including actual payoff month, interest saved,
                        or default exposure and Loss Given Default (LGD).
    """
    if months <= 0:
        raise ValueError("Months must be positive.")

    base_payment = monthly_payment(principal, annual_rate, months)
    monthly_rate = annual_rate / 12.0 / 100.0
    balance = float(principal)
    total_interest_paid = 0.0
    total_principal_paid = 0.0
    simulated_schedule: List[Dict[str, Any]] = []

    # Map prepayments by month
    prepay_map: Dict[int, float] = {}
    recurring_prepay: float = 0.0

    if prepayments:
        for p in prepayments:
            if p.recurring:
                recurring_prepay += p.amount
            else:
                prepay_map[p.month] = prepay_map.get(p.month, 0.0) + p.amount

    actual_payoff_month = months
    status = "PAID_OFF"
    loss_given_default = 0.0
    recovered_amount = 0.0

    for m in range(1, months + 1):
        if default_month is not None and m >= default_month:
            status = "DEFAULTED"
            actual_payoff_month = m
            loss_given_default = round2(balance * (1.0 - recovery_rate))
            recovered_amount = round2(balance * recovery_rate)
            break

        if balance <= 0.0:
            actual_payoff_month = m - 1
            break

        interest = round2(balance * monthly_rate)
        extra = prepay_map.get(m, 0.0) + recurring_prepay
        scheduled_principal = round2(base_payment - interest)

        total_principal_component = scheduled_principal + extra

        if total_principal_component >= balance:
            total_principal_component = balance
            actual_payment = round2(balance + interest)
            balance = 0.0
            actual_payoff_month = m
        else:
            balance = round2(balance - total_principal_component)
            actual_payment = round2(interest + total_principal_component)

        total_interest_paid = round2(total_interest_paid + interest)
        total_principal_paid = round2(total_principal_paid + total_principal_component)

        simulated_schedule.append(
            {
                "month": m,
                "payment": actual_payment,
                "principal_paid": total_principal_component,
                "interest_paid": interest,
                "remaining_balance": balance,
            }
        )

        if balance <= 0.0:
            break

    # Standard baseline interest for comparison
    from finengine.math.amortization import amortize

    baseline = amortize(principal, annual_rate, months)
    interest_saved = round2(max(0.0, baseline.total_interest - total_interest_paid))

    return {
        "status": status,
        "contractual_months": months,
        "actual_payoff_month": actual_payoff_month,
        "months_saved": months - actual_payoff_month if status == "PAID_OFF" else 0,
        "total_principal_paid": total_principal_paid,
        "total_interest_paid": total_interest_paid,
        "interest_saved": interest_saved,
        "default_month": default_month,
        "unpaid_balance_at_default": balance if status == "DEFAULTED" else 0.0,
        "loss_given_default": loss_given_default,
        "recovered_amount": recovered_amount,
        "schedule": simulated_schedule,
    }
