from bond_pricing import price_bond
from yield_solver import solve_ytm
import pytest

def test_bond_prices_at_par():
    price = price_bond(
        face_value=1000,
        coupon_rate=0.05,
        remaining_payments=3,
        annual_yield=0.05,
    )

    assert abs(price - 1000) < 0.000001


def test_zero_coupon_bond():
    price = price_bond(
        face_value=1000,
        coupon_rate=0,
        remaining_payments=2,
        annual_yield=0.1,
    )

    expected_price = 1000 / (1.10 ** 2)

    assert abs(price - expected_price) < 0.000001


def test_zero_yield_bond():
    price = price_bond(
        face_value=1000,
        coupon_rate=0.05,
        remaining_payments=3,
        annual_yield=0
    )

    expected_price = 50+50+50+1000

    assert abs(price - expected_price) < 0.000001


def test_ytm_at_par():
    calculated_yield = solve_ytm(1000, 0.05, 1, 1000)
    expected_yield = 0.05
    assert abs(calculated_yield - expected_yield) < 0.000001

def test_ytm_zero_coupon():
    calculated_yield = solve_ytm(
        face_value=1000, 
        coupon_rate=0,
        remaining_payments=1, 
        market_price=950
    )
    expected_yield = ((1000/950)-1)
    assert(abs(calculated_yield - expected_yield) < 0.000001)

def test_ytm_custom_bounds():
    calculated_yield = solve_ytm(
        face_value=1000,
        coupon_rate=0,
        remaining_payments=1,
        market_price=900,
        lower_yield=0, 
        upper_yield=0.2
    )
    expected_yield = ((1000/900)-1)
    assert (abs(expected_yield-calculated_yield) < 0.00000001)

def test_ytm_outside_bounds():
    with pytest.raises(ValueError):
        solve_ytm(
            face_value=1000,
            coupon_rate=0,
            remaining_payments=1,
            market_price=900,
            lower_yield=0.04,
            upper_yield=0.08
        )


def test_price_falls_when_yield_rises():
    price_at_lower_yield = price_bond(
        face_value=1000, 
        coupon_rate=0.05,
        remaining_payments=3, 
        annual_yield=0.04
    )
    price_at_higher_yield = price_bond(
        face_value=1000,
        coupon_rate=0.05,
        remaining_payments=3, 
        annual_yield=0.06
    )

    assert (price_at_higher_yield < price_at_lower_yield)

def test_ytm_recovers_known_yield():
    market_price = price_bond(
        face_value=1000,
        coupon_rate=0.05,
        remaining_payments=3,
        annual_yield=0.065, 
        coupon_frequency=2
    )
    calculated_yield = solve_ytm(
        face_value=1000,
        coupon_rate=0.05,
        remaining_payments=3,
        market_price=market_price,
        coupon_frequency=2
    )

    assert (abs(calculated_yield-0.065) < 0.00000001)
