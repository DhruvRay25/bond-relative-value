from bond_settlement import calculate_actual_fraction, calculate_30_360_fraction
from datetime import date
import pytest 

def test_settlement_before_coupon_rejected():
    last_coupon_date = date(2026, 1, 15)
    settlement_date = date(2026, 1, 14)
    next_coupon_date = date(2026, 7, 15)

    with pytest.raises(ValueError):
        calculate_actual_fraction(
            last_coupon_date=last_coupon_date,
            settlement_date=settlement_date,
            next_coupon_date=next_coupon_date
        )


def test_fraction_zero_on_coupon_date():
    last_coupon_date = date(2026, 1, 15)
    settlement_date = date(2026, 1, 15)
    next_coupon_date = date(2026, 7, 15)
    fraction = calculate_actual_fraction(
        last_coupon_date=last_coupon_date,
        settlement_date=settlement_date,
        next_coupon_date=next_coupon_date
    )

    assert fraction == 0

def test_30_360_fraction_between_coupons():
    fraction = calculate_30_360_fraction(
        date(2035, 5, 15),
        date(2035, 6, 15),
        date(2035, 11, 15),
    )
    assert fraction == pytest.approx(1 / 6)

def test_30_360_rejects_settlement_on_next_coupon_date():
    with pytest.raises(ValueError):
        calculate_30_360_fraction(
            date(2035, 5, 15),
            date(2035, 11, 15),
            date(2035, 11, 15),
        )

