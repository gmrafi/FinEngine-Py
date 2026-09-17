"""Pandas and tabular analytics primitives for loan schedules and portfolios."""

from __future__ import annotations

from typing import Any, Iterable, List, Sequence, Union
from finengine.math.amortization import AmortizationPlan, AmortizationRow, amortize
from finengine.math.money import round2


def to_dataframe(schedule_or_plan: Union[AmortizationPlan, Sequence[AmortizationRow], Sequence[dict[str, Any]]]) -> Any:
    """Convert an AmortizationPlan, list of AmortizationRow, or row dicts into a pandas DataFrame.

    Args:
        schedule_or_plan: AmortizationPlan object, list of AmortizationRow, or dict records.

    Returns:
        pandas.DataFrame: Tabular DataFrame ready for analysis, plotting, or export.
    """
    try:
        import pandas as pd
    except ImportError as e:
        raise ImportError(
            "Pandas is required for `to_dataframe()`. Install with `pip install finengine[analysis]` or `pip install pandas`."
        ) from e

    if isinstance(schedule_or_plan, AmortizationPlan):
        rows = [r.to_dict() for r in schedule_or_plan.schedule]
    elif isinstance(schedule_or_plan, (list, tuple)):
        rows = [
            r.to_dict() if isinstance(r, AmortizationRow) else dict(r)  # type: ignore[arg-type]
            for r in schedule_or_plan
        ]
    else:
        raise TypeError(f"Unsupported schedule type: {type(schedule_or_plan)}")

    return pd.DataFrame(rows)


def batch_amortize(portfolio: Iterable[dict[str, Any]]) -> Any:
    """Compute amortization schedules and summary metrics across a portfolio of loans.

    Args:
        portfolio: List of loan dicts, each containing:
            - 'id' or 'loan_id' (optional identifier)
            - 'principal' (float)
            - 'annual_rate' (float)
            - 'months' (int)

    Returns:
        pandas.DataFrame: Combined DataFrame containing all loan schedules with loan IDs.
    """
    try:
        import pandas as pd
    except ImportError as e:
        raise ImportError(
            "Pandas is required for `batch_amortize()`. Install with `pip install finengine[analysis]`."
        ) from e

    all_records: List[dict[str, Any]] = []

    for index, loan in enumerate(portfolio):
        loan_id = loan.get("id") or loan.get("loan_id") or f"LOAN_{index + 1:04d}"
        principal = float(loan["principal"])
        annual_rate = float(loan["annual_rate"])
        months = int(loan["months"])

        plan = amortize(principal=principal, annual_rate=annual_rate, months=months)

        for row in plan.schedule:
            rec = row.to_dict()
            rec["loan_id"] = loan_id
            rec["annual_rate"] = annual_rate
            all_records.append(rec)

    return pd.DataFrame(all_records)


def portfolio_summary(portfolio: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Calculate aggregate portfolio-level actuarial metrics.

    Args:
        portfolio: List of loan dicts with principal, annual_rate, months.

    Returns:
        dict: Summary containing total principal, total interest, total monthly cashflow,
              and Weighted Average Interest Rate (WAIR).
    """
    total_principal = 0.0
    total_interest = 0.0
    total_monthly_cashflow = 0.0
    weighted_rate_sum = 0.0
    loan_count = 0

    for loan in portfolio:
        p = float(loan["principal"])
        r = float(loan["annual_rate"])
        m = int(loan["months"])

        plan = amortize(principal=p, annual_rate=r, months=m)
        total_principal += p
        total_interest += plan.total_interest
        total_monthly_cashflow += plan.monthly_payment
        weighted_rate_sum += p * r
        loan_count += 1

    wair = (weighted_rate_sum / total_principal) if total_principal > 0 else 0.0

    return {
        "loan_count": loan_count,
        "total_principal": round2(total_principal),
        "total_interest": round2(total_interest),
        "total_payable": round2(total_principal + total_interest),
        "total_monthly_inflow": round2(total_monthly_cashflow),
        "weighted_average_interest_rate": round2(wair),
    }
