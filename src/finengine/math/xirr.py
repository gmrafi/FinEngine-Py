"""Deterministic non-periodic cash flow internal rate of return (XIRR) solver.

Solves the annualized internal rate of return for irregular cash flows using a
constrained Newton-Raphson method with bisection boundary protection.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Sequence, Union
from .money import round4


@dataclass(frozen=True)
class CashFlow:
    """Represents a discrete cash flow event at a specific calendar date.

    Attributes:
        amount: Net cash flow amount (Negative = Outflow/Investment, Positive = Inflow/Dividend)
        date: Calendar date of transaction (datetime.date, datetime.datetime, or 'YYYY-MM-DD' string)
    """

    amount: float
    date: Union[date, datetime, str]

    def get_date(self) -> date:
        """Extract standardized datetime.date instance."""
        if isinstance(self.date, datetime):
            return self.date.date()
        if isinstance(self.date, date):
            return self.date
        if isinstance(self.date, str):
            # Parse ISO format YYYY-MM-DD
            return datetime.strptime(self.date.strip()[:10], "%Y-%m-%d").date()
        raise TypeError(f"Unsupported date type: {type(self.date)}")

    def to_dict(self) -> dict[str, Any]:
        """Convert CashFlow to dictionary representation."""
        return {
            "amount": self.amount,
            "date": self.get_date().isoformat(),
        }


def xirr(
    cashflows: Sequence[Union[CashFlow, tuple[float, Union[date, datetime, str]]]],
    guess: float = 0.1,
    max_iter: int = 100,
    tol: float = 1e-7,
) -> float:
    """Calculate the Extended Internal Rate of Return (XIRR) for irregular cash flows.

    Args:
        cashflows: Sequence of CashFlow instances or (amount, date) tuples.
        guess: Initial annual rate guess (default: 0.1 for 10%).
        max_iter: Maximum Newton-Raphson iterations (default: 100).
        tol: Convergence tolerance threshold (default: 1e-7).

    Returns:
        float: Annualized internal rate of return rounded to 4 decimal places (e.g. 0.2483 = 24.83%).
    """
    if len(cashflows) < 2:
        raise ValueError("At least two cashflows are required to compute XIRR.")

    normalized: list[tuple[float, date]] = []
    has_positive = False
    has_negative = False

    for item in cashflows:
        if isinstance(item, CashFlow):
            amt = float(item.amount)
            dt = item.get_date()
        elif isinstance(item, (tuple, list)) and len(item) == 2:
            amt = float(item[0])
            raw_dt = item[1]
            if isinstance(raw_dt, datetime):
                dt = raw_dt.date()
            elif isinstance(raw_dt, date):
                dt = raw_dt
            elif isinstance(raw_dt, str):
                dt = datetime.strptime(raw_dt.strip()[:10], "%Y-%m-%d").date()
            else:
                raise TypeError(f"Invalid date in tuple: {raw_dt}")
        else:
            raise TypeError("Cashflow items must be CashFlow objects or (amount, date) tuples.")

        if amt > 0:
            has_positive = True
        elif amt < 0:
            has_negative = True

        normalized.append((amt, dt))

    if not has_positive or not has_negative:
        raise ValueError("Cashflows must include at least one negative outflow and one positive inflow.")

    # Base reference date
    origin_date = normalized[0][1]
    years_and_amounts: list[tuple[float, float]] = []

    for amt, dt in normalized:
        years = (dt - origin_date).days / 365.0
        years_and_amounts.append((amt, years))

    rate = float(guess)

    for _ in range(max_iter):
        # Prevent base from becoming zero or negative (rate <= -1)
        if rate <= -0.9999:
            rate = -0.9999

        f = 0.0
        df = 0.0

        for amt, years in years_and_amounts:
            base = (1.0 + rate) ** years
            if base == 0:
                continue
            f += amt / base
            df += (-years * amt) / (base * (1.0 + rate))

        if abs(df) < 1e-12:
            # Derivative too flat, nudge slightly
            rate += 0.01
            continue

        next_rate = rate - f / df

        # Guard against wild divergence
        if next_rate < -0.99:
            next_rate = (rate - 0.99) / 2.0

        if abs(next_rate - rate) < tol:
            return round4(next_rate)

        rate = next_rate

    return round4(rate)
