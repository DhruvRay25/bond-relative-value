from bond_risk import calculate_duration, calculate_dv01

def test_zero_coupon_duration():
    calculated_duration = calculate_duration(
        face_value=1000,
        coupon_rate=0,
        remaining_payments=3,
        annual_yield=0.06,
        coupon_frequency=1
        )
    expected_duration = 3 / 1.06

    assert abs(calculated_duration - expected_duration) < 0.000001


def test_zero_coupon_dv01():
    calculated_dv01 = calculate_dv01(
        face_value=1000,
        coupon_rate=0, 
        remaining_payments=3, 
        annual_yield=0.06,
        coupon_frequency=1
    )

    expected_price = (1000/(1.06**3))
    expected_duration = 3/(1.06)
    expected_dv01 = expected_duration * expected_price * 0.0001
    assert abs(expected_dv01 - calculated_dv01) < 0.000001


def test_duration_between_coupon_dates():
    calculated_duration = calculate_duration(
        face_value=1000,
        coupon_rate=0,
        remaining_payments=1, 
        annual_yield=0.06,
        coupon_frequency=1,
        fraction_elapsed=0.5
    )

    expected_duration = 0.5/(1.06)

    assert abs(calculated_duration-expected_duration) < 0.000001


def test_dv01_between_coupon_dates():
    calculated_dv01 = calculate_dv01(
        face_value=1000,
        coupon_rate=0,
        remaining_payments=1, 
        annual_yield=0.06,
        coupon_frequency=1,
        fraction_elapsed=0.5
    )

    expected_price = 1000/(1.06)**0.5
    expected_duration = 0.5/1.06
    expected_dv01 = (expected_price)*expected_duration*0.0001

    assert abs(calculated_dv01-expected_dv01) < 0.000001