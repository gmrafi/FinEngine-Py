"""Tests for alternative credit risk and MFS scoring engine."""

from finengine import (
    MFSProfile,
    assess_credit_risk,
)


def test_high_credit_profile() -> None:
    """Test credit assessment for strong transactional profile."""
    profile = MFSProfile(
        monthly_inflows=75000,
        monthly_outflows=35000,
        avg_balance=20000,
        transaction_frequency=45,
        utility_bill_consistency=1.0,
        account_age_months=36,
        past_defaults=0,
        volatility_index=0.15,
    )
    result = assess_credit_risk(profile=profile)
    assert 700 <= result.score <= 850
    assert result.default_probability < 0.15
    assert result.risk_tier in ("LOW", "MEDIUM")
    assert result.recommended_credit_limit > 50000


def test_high_risk_profile() -> None:
    """Test credit assessment for delinquent/over-leveraged profile."""
    profile = MFSProfile(
        monthly_inflows=20000,
        monthly_outflows=22000,
        avg_balance=500,
        transaction_frequency=3,
        utility_bill_consistency=0.5,
        account_age_months=4,
        past_defaults=2,
        volatility_index=0.75,
    )
    result = assess_credit_risk(profile=profile)
    assert result.score < 600
    assert result.default_probability > 0.40
    assert result.risk_tier in ("HIGH", "CRITICAL")
    assert len(result.reasons) > 0


def test_cashflow_assessment() -> None:
    """Test credit risk scoring directly from inflow time series."""
    inflows = [50000, 52000, 48000, 51000, 53000, 49000]
    result = assess_credit_risk(inflows=inflows)
    assert 300 <= result.score <= 850
    assert 0.0 <= result.default_probability <= 1.0
    assert result.recommended_credit_limit > 0
