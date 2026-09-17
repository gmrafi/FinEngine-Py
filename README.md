# FinEngine-Py

[![PyPI Version](https://img.shields.io/pypi/v/finengine?color=3775A9&logo=pypi&logoColor=white)](https://pypi.org/project/finengine/)
[![Python Versions](https://img.shields.io/pypi/pyversions/finengine?color=blue&logo=python&logoColor=white)](https://pypi.org/project/finengine/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/gmrafi/FinEngine-Py/blob/main/LICENSE)
[![DOI](https://img.shields.io/badge/DOI-10.67226%2Fcfsbr.fe.2026.001.v1-blue)](https://doi.org/10.67226/cfsbr.fe.2026.001.v1)
[![Zenodo DOI](https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.22769502-blue.svg)](https://doi.org/10.5281/zenodo.22769502)
[![Strict Typing](https://img.shields.io/badge/typing-strict%20hints-success)](https://github.com/gmrafi/FinEngine-Py)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**Deterministic financial math, IEEE-754 float drift mitigation, actuarial amortization, and alternative credit risk modeling for Python.**

A computational research initiative by the **Centre for Fintech & Strategic Business Research (CFSBR)**.

[Key Guarantees](#key-guarantees) · [Ecosystem](#monorepo-packages--cross-platform-ecosystem) · [Installation](#installation) · [Quickstart](#quickstart-examples) · [Live Surfaces](#live-interactive-surfaces) · [Citation](#academic-backing--citation) · [Development](#local-development--testing)

---

## Why FinEngine for Python?

Modern quantitative finance, fintech backend services, and machine learning credit models require absolute numerical precision. Standard IEEE-754 double-precision floating-point arithmetic introduces non-linear representation drift:

```python
0.1 + 0.2 == 0.3  # False in standard float (0.30000000000000004)
```

In multi-period loan amortization schedules, interest compounding, and portfolio ledgers, this drift compounds non-linearly across time horizons, causing final closing balances to fail to liquidate cleanly to zero ($B_n \neq 0.00$).

**FinEngine-Py** provides a zero-dependency, deterministic integer-scaled arithmetic architecture with native support for South Asian currency conventions (Bangladeshi Taka · Poisha), strict type hints, Pandas DataFrame integration, and alternative credit risk scoring.

---

## Key Guarantees

- **Zero Float Drift**: Replaces standard Python float rounding issues with integer-scaled monetary sub-unit arithmetic (Poisha / Cents: 1 BDT = 100 Poisha).
- **Terminal Reconciliation Rule**: Mathematical boundary enforcement guaranteeing the closing principal balance strictly liquidates to exactly zero ($B_n \equiv 0.00$).
- **Actuarial Loan Amortization**: True reducing-balance Equated Monthly Installment (EMI) schedules with monthly principal and interest splits.
- **Advanced Financial Solvers**: Constrained Newton-Raphson solvers with binary bisection fallbacks for non-periodic cash flow internal rate of return (XIRR).
- **Alternative Credit Risk AI**: Lightweight pre-calibrated scoring models for Microfinance, MFS (bKash/Nagad/Rocket), and SME nano-loans.
- **Data Science Ready**: Direct, zero-boilerplate export to structured `pandas.DataFrame` objects for Jupyter Notebooks, plotting, and Excel pipelines.
- **100% Pure Python**: Zero C-compilation dependencies. Runs seamlessly on AWS Lambda, Google Cloud Functions, PyPy, Jupyter, and Edge runtimes.

---

## Monorepo Packages & Cross-Platform Ecosystem

FinEngine maintains identical mathematical parity between client-side JavaScript runtimes and Python scientific backends:

| Package | Version | Registry | Purpose | Key Exports |
| :--- | :--- | :--- | :--- | :--- |
| [`@finengine/core`](https://github.com/gmrafi/FinEngine/blob/main/packages/core) | `0.3.0` | npm | Integer sub-unit arithmetic, BDT currency primitives, and ledger validators. | `createMoney`, `formatMoney`, `validateLedgerEntry` |
| [`@finengine/math`](https://github.com/gmrafi/FinEngine/blob/main/packages/math) | `0.3.0` | npm | Actuarial reducing-balance loan amortization and XIRR solvers. | `amortize`, `monthlyPayment`, `xirr` |
| [`@finengine/ui`](https://github.com/gmrafi/FinEngine/blob/main/packages/ui) | `0.3.0` | npm | Accessible UI view-models for repayment summaries and burden gauges. | `makeMoneyKpi`, `makeRepaymentSummary` |
| [**`finengine`**](https://pypi.org/project/finengine/) | `0.1.0` | PyPI | Python actuarial math, integer Poisha scaling, Pandas DataFrames, and credit AI. | `amortize`, `to_dataframe`, `xirr`, `assess_credit_risk` |

---

## Installation

```bash
# 1. Minimal installation (Zero dependencies, 100% pure math)
pip install finengine

# 2. With Pandas & NumPy DataFrame support
pip install "finengine[analysis]"

# 3. Full suite with AI & alternative credit risk models
pip install "finengine[all]"
```

---

## Quickstart Examples

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

### 5. Loan Stress-Testing & Prepayment Acceleration

```python
from finengine.analytics import Prepayment, simulate_loan

# Simulate loan with an extra BDT 1,00,000 lump-sum prepayment at month 12
result = simulate_loan(
    principal=500000,
    annual_rate=13.5,
    months=36,
    prepayments=[Prepayment(month=12, amount=100000)],
)

print(f"Actual Payoff Month: {result['actual_payoff_month']} (Saved {result['months_saved']} months)")
print(f"Total Interest Saved: BDT {result['interest_saved']:,.2f}")
```

---

## Live Interactive Surfaces

Explore FinEngine live in your browser:

- **Flagship Portal**: [https://finengine.js.org/](https://finengine.js.org/)
- **Python SDK & Quant Hub**: [https://finengine.js.org/python/](https://finengine.js.org/python/)
- **Live Loan Simulator**: [https://finengine.js.org/#interactive-simulator](https://finengine.js.org/#interactive-simulator)
- **VS Code Precision Playground**: [https://finengine.js.org/#precision-playground](https://finengine.js.org/#precision-playground)
- **Full Simulation Lab**: [https://finengine.js.org/simulation/](https://finengine.js.org/simulation/)
- **Technical Working Paper (Methodology)**: [https://finengine.js.org/methodology/](https://finengine.js.org/methodology/)
- **API Documentation**: [https://finengine.js.org/docs/](https://finengine.js.org/docs/)

---

## Local Development & Testing

```bash
# Clone the repository
git clone https://github.com/gmrafi/FinEngine-Py.git
cd FinEngine-Py

# Install in editable mode with development & analysis dependencies
pip install -e ".[dev,all]"

# Run test suite
pytest -v tests/

# Type check with mypy
mypy src/

# Lint with ruff
ruff check src/ tests/
```

---

## Academic Backing & Citation

FinEngine is published as an open computational methodology standard by the **Centre for Fintech and Strategic Business Research (CFSBR)**.

### APA 7th Edition
> Rafi, M. G. M. (2026). *FinEngine: A Deterministic Computational Framework for Client-Side Financial Interfaces* (CFSBR Technical Working Paper No. CFSBR-FE-2026-001). Centre for Fintech and Strategic Business Research. https://doi.org/10.67226/cfsbr.fe.2026.001.v1

### BibTeX (Working Paper)
```bibtex
@techreport{rafi2026finengine,
  author      = {Rafi, Md Golam Mubasshir},
  title       = {FinEngine: A Deterministic Computational Framework for Client-Side Financial Interfaces},
  institution = {Centre for Fintech and Strategic Business Research (CFSBR)},
  year        = {2026},
  month       = {September},
  type        = {Technical Working Paper},
  number      = {CFSBR-FE-2026-001},
  doi         = {10.67226/cfsbr.fe.2026.001.v1},
  url         = {https://finengine.js.org/methodology/}
}
```

### BibTeX (Software Archive · CERN Zenodo)
```bibtex
@software{finengine_core_v030,
  author    = {Rafi, Md Golam Mubasshir},
  title     = {gmrafi/FinEngine: FinEngine v0.3.0: The Deterministic Financial Engine Release},
  year      = {2026},
  publisher = {Zenodo},
  version   = {v0.3.0},
  doi       = {10.5281/zenodo.22769502},
  url       = {https://doi.org/10.5281/zenodo.22769502}
}
```

### Archival Identifiers
- **Methodology DOI (Crossref)**: [10.67226/cfsbr.fe.2026.001.v1](https://doi.org/10.67226/cfsbr.fe.2026.001.v1)
- **Software Version DOI (Zenodo)**: [10.5281/zenodo.22769502](https://doi.org/10.5281/zenodo.22769502)
- **Software Concept DOI (Zenodo All Versions)**: [10.5281/zenodo.22769501](https://doi.org/10.5281/zenodo.22769501)
- **Software Heritage ID**: `swh:1:dir:4da6366919f478fd431b2f9ce1d342620cc8834f`

---

## License

- **Software Code**: [MIT License](LICENSE) © 2026 Md Golam Mubasshir Rafi / FinEngine Labs.
- **Documentation & Research Methodology**: [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
