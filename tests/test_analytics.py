"""Analytics and portfolio simulation tests."""

from finengine import (
    Prepayment,
    portfolio_summary,
    simulate_loan,
)


def test_portfolio_summary() -> None:
    """Test portfolio aggregation metrics."""
    portfolio = [
        {"principal": 500000, "annual_rate": 13.5, "months": 36},
        {"principal": 300000, "annual_rate": 12.0, "months": 24},
    ]
    summary = portfolio_summary(portfolio)
    assert summary["loan_count"] == 2
    assert summary["total_principal"] == 800000.00
    assert summary["total_interest"] > 0
    assert summary["total_payable"] == summary["total_principal"] + summary["total_interest"]
    assert 12.0 <= summary["weighted_average_interest_rate"] <= 13.5


def test_prepayment_simulation() -> None:
    """Test loan simulation with extra lump-sum prepayment."""
    res = simulate_loan(
        principal=500000,
        annual_rate=13.5,
        months=36,
        prepayments=[Prepayment(month=12, amount=100000)],
    )
    assert res["status"] == "PAID_OFF"
    assert res["actual_payoff_month"] < 36
    assert res["months_saved"] > 0
    assert res["interest_saved"] > 0


def test_default_simulation() -> None:
    """Test loan simulation under borrower default scenario."""
    res = simulate_loan(
        principal=500000,
        annual_rate=13.5,
        months=36,
        default_month=15,
        recovery_rate=0.20,
    )
    assert res["status"] == "DEFAULTED"
    assert res["default_month"] == 15
    assert res["unpaid_balance_at_default"] > 0
    assert res["loss_given_default"] > 0
    assert res["recovered_amount"] > 0
    assert (
        round(res["loss_given_default"] + res["recovered_amount"], 2)
        == round(res["unpaid_balance_at_default"], 2)
    )
