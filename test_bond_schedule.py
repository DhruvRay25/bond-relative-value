from datetime import date
from bond_schedule import build_coupon_schedule

def test_settlement_on_coupon_date():
    maturity_date = date(2036, 5, 15)
    settlement_date = date(2035, 11, 15)  # This is a coupon date

    previous_coupon_date, coupon_dates = build_coupon_schedule(maturity_date, settlement_date)

    assert previous_coupon_date == settlement_date
    expected_dates = [date(2036, 5, 15)]
    assert coupon_dates == expected_dates
    