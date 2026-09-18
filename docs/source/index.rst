Welcome to FinEngine's Python API Documentation!
================================================

.. note::
   For the central platform, interactive visual simulators, and client-side JavaScript packages, visit `finengine.js.org <https://finengine.js.org>`_.

Getting Started
---------------

**FinEngine-Py** provides audited actuarial math, integer-scaled sub-unit arithmetic, and credit risk AI for Python.

Installation
^^^^^^^^^^^^

Install the pure-math core with zero dependencies:

.. code-block:: bash

    pip install finengine

For Pandas integration and advanced analytics, install with extras:

.. code-block:: bash

    pip install "finengine[analysis]"

Quick Example
^^^^^^^^^^^^^

.. code-block:: python

    from finengine import amortize, format_money

    # Compute a 36-month loan amortization for BDT 5,00,000 at 13.5% p.a.
    plan = amortize(principal=500000, annual_rate=13.5, months=36)

    print(f"Monthly Payment: {format_money(plan.monthly_payment, 'BDT')}")
    # -> Monthly Payment: BDT 16,967.64

    print(f"Final Balance: {plan.schedule[-1].remaining_balance}")
    # -> Final Balance: 0.0 (Guaranteed Terminal Zero Closure)

API Reference
=============

.. toctree::
   :maxdepth: 2
   :caption: Modules:

Mathematical Primitives
-----------------------
.. automodule:: finengine.math
   :members:
   :undoc-members:
   :show-inheritance:

Quantitative Analytics
----------------------
.. automodule:: finengine.analytics
   :members:
   :undoc-members:
   :show-inheritance:

Credit Risk AI
--------------
.. automodule:: finengine.ai
   :members:
   :undoc-members:
   :show-inheritance:
