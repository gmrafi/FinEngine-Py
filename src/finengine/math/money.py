"""Deterministic monetary primitives and integer sub-unit arithmetic.

Eliminates IEEE-754 floating point drift by maintaining exact integer sub-unit
representations (Poisha / Cents: 1 unit = 100 sub-units).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Union

SupportedCurrency = Literal["BDT", "USD", "EUR", "GBP"]


def round2(value: float) -> float:
    """Rounds a float to 2 decimal places with epsilon drift protection."""
    # Matches JavaScript round2: Math.round((value + Number.EPSILON) * 100) / 100
    return round(float(value) + 1e-12, 2)


def round4(value: float) -> float:
    """Rounds a float to 4 decimal places with epsilon drift protection."""
    return round(float(value) + 1e-12, 4)


@dataclass(frozen=True)
class Money:
    """Represents a deterministic monetary value anchored to integer sub-units.

    Attributes:
        amount: Standard decimal currency representation (e.g. 1500.50)
        currency: ISO 4217 Currency code (default: 'BDT')
        sub_units: Exact integer sub-units (e.g. 150050 Poisha/Cents)
    """

    amount: float
    currency: str = "BDT"
    sub_units: int = 0

    def __post_init__(self) -> None:
        if not self.sub_units and self.amount != 0:
            object.__setattr__(self, "sub_units", int(round(self.amount * 100)))
        elif self.sub_units != 0 and self.amount == 0.0:
            object.__setattr__(self, "amount", round2(self.sub_units / 100.0))

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "amount": self.amount,
            "currency": self.currency,
            "sub_units": self.sub_units,
        }

    def __repr__(self) -> str:
        return f"Money(amount={self.amount:.2f}, currency='{self.currency}', sub_units={self.sub_units})"

    def __str__(self) -> str:
        return format_money(self.amount, self.currency)

    def __add__(self, other: Union[Money, float, int]) -> Money:
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError(
                    f"Cannot add different currencies: {self.currency} and {other.currency}"
                )
            new_sub_units = self.sub_units + other.sub_units
            return Money(amount=round2(new_sub_units / 100.0), currency=self.currency, sub_units=new_sub_units)
        new_amount = round2(self.amount + float(other))
        return create_money(new_amount, self.currency)

    def __sub__(self, other: Union[Money, float, int]) -> Money:
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError(
                    f"Cannot subtract different currencies: {self.currency} and {other.currency}"
                )
            new_sub_units = self.sub_units - other.sub_units
            return Money(amount=round2(new_sub_units / 100.0), currency=self.currency, sub_units=new_sub_units)
        new_amount = round2(self.amount - float(other))
        return create_money(new_amount, self.currency)

    def __mul__(self, scalar: Union[float, int]) -> Money:
        new_sub_units = int(round(self.sub_units * float(scalar)))
        return Money(amount=round2(new_sub_units / 100.0), currency=self.currency, sub_units=new_sub_units)


def create_money(amount: float, currency: str = "BDT") -> Money:
    """Create a Money object with integer sub-unit scaling."""
    r_amt = round2(amount)
    sub_units = int(round(r_amt * 100))
    return Money(amount=r_amt, currency=currency, sub_units=sub_units)


def _format_south_asian(integer_part: int) -> str:
    """Format an integer with South Asian (Lakh / Crore: 3,2,2...) comma separators."""
    s = str(abs(integer_part))
    if len(s) <= 3:
        return s
    last_three = s[-3:]
    remaining = s[:-3]
    chunks = []
    while len(remaining) > 2:
        chunks.append(remaining[-2:])
        remaining = remaining[:-2]
    if remaining:
        chunks.append(remaining)
    chunks.reverse()
    return ",".join(chunks) + "," + last_three


def format_money(amount: float, currency: str = "BDT", locale: str = "en-BD") -> str:
    """Format a monetary float into standardized locale-aware currency strings.

    Args:
        amount: Monetary number (e.g. 500000)
        currency: ISO 4217 Currency code ('BDT', 'USD', etc.)
        locale: Target locale ('en-BD', 'en-US', etc.)

    Returns:
        Formatted string (e.g. 'BDT 5,00,000.00' or '$500,000.00')
    """
    val = round2(amount)
    is_negative = val < 0
    abs_val = abs(val)

    int_part = int(abs_val)
    frac_part = int(round((abs_val - int_part) * 100))

    if locale in ("en-BD", "bn-BD") or currency == "BDT":
        formatted_int = _format_south_asian(int_part)
    else:
        formatted_int = f"{int_part:,}"

    sign = "-" if is_negative else ""
    formatted_num = f"{sign}{formatted_int}.{frac_part:02d}"

    if currency == "USD" and locale == "en-US":
        return f"${formatted_num}"
    if currency == "EUR":
        return f"€{formatted_num}"
    if currency == "GBP":
        return f"£{formatted_num}"
    return f"{currency} {formatted_num}"
