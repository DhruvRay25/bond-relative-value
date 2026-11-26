from bond_pricing import price_bond

def calculate_duration(face_value, coupon_rate, remaining_payments, annual_yield, coupon_frequency = 1, fraction_elapsed=0.0):
    yield_bump = 0.0001
    base_price = price_bond(face_value, coupon_rate, remaining_payments, annual_yield, coupon_frequency, fraction_elapsed=fraction_elapsed)

    price_down = price_bond(face_value, coupon_rate, remaining_payments, (annual_yield - yield_bump), coupon_frequency, fraction_elapsed=fraction_elapsed)

    price_up = price_bond(face_value, coupon_rate, remaining_payments, (annual_yield + yield_bump), coupon_frequency, fraction_elapsed=fraction_elapsed)

    modified_duration = (price_down-price_up)/(2*base_price*yield_bump)

    return modified_duration

def calculate_dv01(face_value, coupon_rate, remaining_payments, annual_yield, coupon_frequency = 1, fraction_elapsed=0.0):
    bond_price = price_bond(face_value, coupon_rate, remaining_payments, annual_yield, coupon_frequency, fraction_elapsed=fraction_elapsed)
    modified_duration = calculate_duration(face_value, coupon_rate, remaining_payments, annual_yield, coupon_frequency, fraction_elapsed=fraction_elapsed)
    dv01 = (modified_duration * bond_price * 0.0001)
    return dv01


if __name__ == "__main__":
    duration = calculate_duration(
        face_value=1000, 
        coupon_rate=0,
        years_to_maturity=3, 
        annual_yield=0.06, 
        coupon_frequency=1
    )
    bond_dv01 = calculate_dv01(
        face_value=1000,
        coupon_rate=0, 
        years_to_maturity=3,
        annual_yield=0.06,
        coupon_frequency=1, 
        
    )

    original_price = price_bond(
        face_value=1000,
        coupon_rate=0,
        years_to_maturity=3, 
        annual_yield=0.06,
        coupon_frequency=1
    )

    higher_yield_price = price_bond(
        face_value=1000,
        coupon_rate=0,
        years_to_maturity=3, 
        annual_yield=0.061,
        coupon_frequency=1
    )
    
    actual_price_loss = original_price - higher_yield_price

    print(f"Modified duration: {duration:.6f}")
    print(f"DV01: ${bond_dv01:.6f}")
    print(f"Actual 1 bp price loss: ${actual_price_loss:.6f}")
    print(f"DV01 estimate: ${bond_dv01:.6f}")