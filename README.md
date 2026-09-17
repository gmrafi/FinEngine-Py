# FinEngine-Py

[![PyPI Version](https://img.shields.io/badge/pypi-v0.1.0-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/finengine/)
[![Python Versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?logo=python&logoColor=white)](https://pypi.org/project/finengine/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/gmrafi/FinEngine-Py/blob/main/LICENSE)
[![Strict Typing](https://img.shields.io/badge/typing-strict%20hints-success)](https://github.com/gmrafi/FinEngine-Py)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**Deterministic Financial Math, Credit Risk Modeling, and Quantitative Primitives for Python.**

A computational research initiative by the **Centre for Fintech & Strategic Business Research (CFSBR)**.

---

## 🌟 Overview & Philosophy

**FinEngine-Py** brings audited actuarial math, integer-scaled sub-unit arithmetic (Poisha / Cents), strict type hints, and Pandas DataFrame integration to Python quants, data scientists, and fintech developers.

- **Zero-Dependency Math Core**: The `finengine.math` module is 100% pure Python with zero third-party dependencies.
- **Float-Drift Elimination**: Protects accounting ledgers against IEEE-754 floating-point drift using integer sub-unit scaling.
- **Terminal Zero Reconciliation Rule**: Guarantees that the final loan amortization installment strictly liquidates to exactly `0.00`.
- **Cross-Platform Parity**: Models prototyped in Python yield 100% identical mathematical output to the [FinEngine TypeScript/JavaScript engine](https://finengine.js.org).
- **Alternative Credit Risk AI**: Lightweight pre-calibrated scoring models for Microfinance, MFS (bKash/Nagad), and SME nano-loans.

---

## 🚀 Installation

```bash
# Minimal installation (Zero dependencies, pure math)
pip install finengine

# With Pandas & NumPy DataFrame support
pip install "finengine[analysis]"

# With Scikit-Learn AI & Risk modeling support
pip install "finengine[all]"
```

---

## 💡 Code Recipes & Examples

### 1. Deterministic Loan Amortization (36-Month EMI)

```python
from finengine import amortize, format_money

# Compute a 36-month loan amortization for BDT 5,00,000 at 13.5% p.a.
plan = amortize(principal=500000, annual_rate=13.5, months=36)

print(f"Monthly Payment: {format_money(plan.monthly_payment, 'BDT')}")
# → Monthly Payment: BDT 16,967.64

print(f"Total Interest:  {format_money(plan.total_interest, 'BDT')}")
# → Total Interest:  BDT 1,10,835.20

print(f"Final Balance:   {plan.schedule[-1].remaining_balance}")
# → Final Balance:   0.0 (Guaranteed Terminal Zero Closure)
```

---

### 2. Tabular Pandas DataFrame Schedule Analysis

```python
import pandas as pd
from finengine import amortize, to_dataframe

plan = amortize(principal=500000, annual_rate=13.5, months=36)

# Direct conversion into structured Pandas DataFrame
df = to_dataframe(plan)
print(df.head())
#    month   payment  principal_paid  interest  remaining_balance
# 0      1  16967.64        11342.64   5625.00          488657.36
# 1      2  16967.64        11470.25   5497.39          477187.11
# 2      3  16967.64        11599.29   5368.35          465587.82

# Export to spreadsheet format
df.to_csv("sme_amortization_schedule.csv", index=False)
```

---

### 3. Non-Periodic Cash Flow XIRR Solver

```python
from datetime import date
from finengine import xirr, CashFlow

cashflows = [
    CashFlow(amount=-100000, date=date(2026, 1, 1)),   # Initial investment
    CashFlow(amount=25000,  date=date(2026, 4, 1)),   # Q1 Dividend
    CashFlow(amount=30000,  date=date(2026, 8, 15)),  # Q2 Distribution
    CashFlow(amount=65000,  date=date(2026, 12, 31)), # Year-end liquidation
]

rate = xirr(cashflows)
print(f"Annualized Internal Rate of Return (XIRR): {rate * 100:.2f}%")
# → Annualized Internal Rate of Return (XIRR): 24.83%
```

---

### 4. Alternative Credit Risk & MFS Nano-Loan Scoring

```python
from finengine.ai import MFSProfile, assess_credit_risk

profile = MFSProfile(
    monthly_inflows=75000.0,
    monthly_outflows=35000.0,
    avg_balance=18000.0,
    transaction_frequency=40,
    utility_bill_consistency=1.0,
    account_age_months=24,
    past_defaults=0,
)

assessment = assess_credit_risk(profile=profile, requested_amount=50000)

print(f"Credit Score:      {assessment.score} / 850")
print(f"Default Risk (PD): {assessment.default_probability * 100:.2f}%")
print(f"Risk Tier:         {assessment.risk_tier}")
print(f"Recommended Limit: BDT {assessment.recommended_credit_limit:,.2f}")
```

---

## 📊 API Reference

| Function / Class | Signature | Return Type | Description |
| :--- | :--- | :--- | :--- |
| `amortize()` | `(principal, annual_rate, months, round_to_integer=False)` | `AmortizationPlan` | Computes full reducing-balance EMI schedule with Terminal Zero guarantee. |
| `monthly_payment()` | `(principal, annual_rate, months, round_to_integer=False)` | `float` | Returns exact monthly installment amount. |
| `xirr()` | `(cashflows, guess=0.1, max_iter=100)` | `float` | Solves annualized internal rate of return for irregular non-periodic cashflows. |
| `create_money()` | `(amount, currency='BDT')` | `Money` | Creates monetary instance with integer sub-unit scaling. |
| `format_money()` | `(amount, currency='BDT', locale='en-BD')` | `str` | Formats currency strings with South Asian (Lakh/Crore) or Western notation. |
| `to_dataframe()` | `(schedule_or_plan)` | `pandas.DataFrame` | Converts plan or schedule rows into a structured DataFrame. |
| `batch_amortize()` | `(portfolio)` | `pandas.DataFrame` | Computes multi-loan portfolio schedules. |
| `simulate_loan()` | `(principal, annual_rate, months, prepayments=None, default_month=None)` | `dict` | Simulates prepayment acceleration or borrower default stress scenarios. |
| `assess_credit_risk()` | `(inflows=None, profile=None, requested_amount=0.0)` | `CreditAssessment` | Evaluates borrower credit risk, score, and safe exposure limit. |

---

## 🛠️ Development & Testing

```bash
# Clone repository
git clone https://github.com/gmrafi/FinEngine-Py.git
cd FinEngine-Py

# Install in editable mode with development dependencies
pip install -e ".[dev,all]"

# Run test suite
pytest -v tests/

# Type check with mypy
mypy src/

# Lint with ruff
ruff check src/ tests/
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).

Copyright (c) 2026 CFSBR Computational Team & Md Golam Mubasshir Rafi.
