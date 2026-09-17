"""Parity tests ensuring 100% mathematical parity between JavaScript and Python engines."""

from datetime import date
from finengine import (
    CashFlow,
    amortize,
    create_money,
    format_money,
    monthly_payment,
    xirr,
)


def test_amortization_parity_values() -> None:
    """Validate 500,000 BDT, 13.5% p.a., 36 months schedule matches JS engine."""
    plan = amortize(principal=500000, annual_rate=13.5, months=36)

    # Monthly payment parity
    assert plan.monthly_payment == 16967.64
    assert monthly_payment(500000, 13.5, 36) == 16967.64
    assert monthly_payment(500000, 13.5, 36, round_to_integer=True) == 16968.0

    # Month 1 installment breakdown
    m1 = plan.schedule[0]
    assert m1.month == 1
    assert m1.payment == 16967.64
    assert m1.interest_paid == 5625.00
    assert m1.interest == 5625.00
    assert m1.principal_paid == 11342.64
    assert m1.remaining_balance == 488657.36

    # Month 2 installment breakdown
    m2 = plan.schedule[1]
    assert m2.month == 2
    assert m2.payment == 16967.64
    assert m2.interest_paid == 5497.39
    assert m2.principal_paid == 11470.25
    assert m2.remaining_balance == 477187.11

    # Totals
    assert plan.total_interest == 110835.20
    assert plan.total_payable == 610835.20

    # Terminal Zero Reconciliation Rule
    final_row = plan.schedule[-1]
    assert final_row.month == 36
    assert final_row.remaining_balance == 0.0


def test_integer_rounded_amortize() -> None:
    """Test integer rounded amortize calculations."""
    plan = amortize(principal=500000, annual_rate=13.5, months=36, round_to_integer=True)
    assert plan.monthly_payment == 16968.0
    m1 = plan.schedule[0]
    assert m1.interest_paid == 5625.00
    assert m1.principal_paid == 11343.00
    assert m1.remaining_balance == 488657.00
    assert plan.schedule[-1].remaining_balance == 0.0


def test_zero_interest_loan() -> None:
    """Ensure zero-interest loans divide principal cleanly."""
    plan = amortize(principal=120000, annual_rate=0.0, months=12)
    assert plan.monthly_payment == 10000.00
    assert plan.total_interest == 0.00
    assert plan.total_payable == 120000.00
    assert plan.schedule[-1].remaining_balance == 0.0


def test_xirr_parity() -> None:
    """Validate XIRR solver produces exact 24.83% for standard cashflow vector."""
    cashflows = [
        CashFlow(amount=-100000, date=date(2026, 1, 1)),
        CashFlow(amount=25000, date=date(2026, 4, 1)),
        CashFlow(amount=30000, date=date(2026, 8, 15)),
        CashFlow(amount=65000, date=date(2026, 12, 31)),
    ]
    rate = xirr(cashflows)
    assert rate == 0.2483


def test_xirr_string_dates() -> None:
    """Validate string date parsing in XIRR."""
    cashflows = [
        CashFlow(amount=-50000, date="2026-01-01"),
        CashFlow(amount=60000, date="2027-01-01"),
    ]
    rate = xirr(cashflows)
    assert rate == 0.2000


def test_money_primitives_and_formatting() -> None:
    """Validate sub-unit money creation and South Asian formatting."""
    m = create_money(500000, "BDT")
    assert m.amount == 500000.0
    assert m.sub_units == 50000000
    assert m.currency == "BDT"

    formatted = format_money(500000, "BDT")
    assert formatted == "BDT 5,00,000.00"

    formatted_emi = format_money(16967.64, "BDT")
    assert formatted_emi == "BDT 16,967.64"

    formatted_interest = format_money(110835.20, "BDT")
    assert formatted_interest == "BDT 1,10,835.20"
