from datetime import date
from bond_pricing import price_bond
from yield_solver import solve_ytm



def calculate_accrued_interest(face_value, coupon_rate, coupon_frequency, fraction_elapsed):
    coupon_payment = (face_value * coupon_rate)/(coupon_frequency)
    accrued_interest = (coupon_payment * fraction_elapsed)
    return accrued_interest

def clean_to_dirty(clean_price, accrued_interest):
    return clean_price + accrued_interest


def calculate_actual_fraction(last_coupon_date, settlement_date, next_coupon_date):
    
    if not (last_coupon_date <= settlement_date < next_coupon_date):
        raise ValueError("Settlement must fall on or after the last coupon date and before the next.")
    
    days_elapsed = (settlement_date - last_coupon_date).days
    days_in_period = (next_coupon_date - last_coupon_date).days
    fraction_elapsed = (days_elapsed/days_in_period)
    return fraction_elapsed


def days_30_360(start_date, end_date):
    years = end_date.year - start_date.year
    months = end_date.month - start_date.month
    days = end_date.day - start_date.day

    return (years*360) + (months*30) + days

def calculate_30_360_fraction(last_coupon_date, settlement_date, next_coupon_date):
    
    if not (last_coupon_date <= settlement_date < next_coupon_date):
        raise ValueError("Settlement must fall on or after the last coupon date and before the next.")
    
    days_elapsed = days_30_360(last_coupon_date, settlement_date)
    days_in_period = days_30_360(last_coupon_date, next_coupon_date)

    return days_elapsed/days_in_period



if __name__ == "__main__":
    example_accrued_interest = calculate_accrued_interest(
        face_value=1000,
        coupon_rate=0.06,
        coupon_frequency=2,
        fraction_elapsed=0.5
    )

    settlement_dirty_price = price_bond(
        face_value=1000,
        coupon_rate=0.06,
        years_to_maturity=1, 
        annual_yield=0.06,
        coupon_frequency=2,
        fraction_elapsed=0.5
    )
    settlement_solved_yield = solve_ytm(
        face_value=1000,
        coupon_rate=0.06,
        years_to_maturity=1, 
        market_price=settlement_dirty_price, 
        coupon_frequency=2,
        fraction_elapsed=0.5
    )
    print(settlement_solved_yield)


    expected_dirty_price = (30/(1.03)**(0.5)) + (1030/(1.03)**(1.5))
    print(f"Settlement dirty price: ${settlement_dirty_price:.6f}")
    print(f"Expected dirty price: ${expected_dirty_price:.6f}")

    settlement_accrued_interest = calculate_accrued_interest(
        face_value=1000,
        coupon_rate=0.06,
        coupon_frequency=2,
        fraction_elapsed=0.5
    )

    settlement_clean_price = settlement_dirty_price - settlement_accrued_interest 
    print(f"Expected clean price: ${settlement_clean_price:.6f}")


    last_coupon_date = date(2026, 1, 15)
    settlement_date = date(2026, 4, 15)
    next_coupon_date = date(2026, 7, 15)

    days_elapsed = (settlement_date - last_coupon_date).days

    days_in_period = (next_coupon_date - last_coupon_date).days
    fraction_elapsed = calculate_actual_fraction(
        last_coupon_date=last_coupon_date,
        settlement_date=settlement_date,
        next_coupon_date=next_coupon_date,
    )

    date_based_accrued = calculate_accrued_interest(
        face_value=1000,
        coupon_rate=0.06,
        coupon_frequency=2, 
        fraction_elapsed=fraction_elapsed
    )

    print(f"Days in period: {days_in_period}")
    print(f"Fraction elapsed: {fraction_elapsed:.6f}")
    print(f"Accrued interest: ${date_based_accrued:.2f}")

    print(days_elapsed)

    common_fractions = [0, 0.25, 0.75]

    for i in common_fractions:
        accrued = calculate_accrued_interest(
            face_value=1000,
            coupon_rate=0.06, 
            coupon_frequency=2, 
            fraction_elapsed=i
        )

        print(f"Fraction: {i:.2f} | Accrued interest: ${accrued:.2f}")

    dirty_price = clean_to_dirty(clean_price=980, accrued_interest=example_accrued_interest)

    print(f"Dirty Price: ${dirty_price:.2f}")

    print(f"Accrued interest: ${example_accrued_interest:.2f}")
    