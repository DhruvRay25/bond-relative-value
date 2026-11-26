from datetime import date
from dateutil.relativedelta import relativedelta
from bond_settlement import calculate_actual_fraction, calculate_accrued_interest, clean_to_dirty, calculate_30_360_fraction
from yield_solver import solve_ytm
from bond_pricing import price_bond


maturity_date = date(2036, 5, 15)
six_months = relativedelta(months=6)

previous_coupon_date = maturity_date - six_months 

print(previous_coupon_date)  # Output: 2035-11-15

def build_coupon_schedule(maturity_date, settlement_date):

    coupon_date = maturity_date
    periods_back = 0

    coupon_dates = []



    while coupon_date > settlement_date:
        coupon_dates.append(coupon_date)
        periods_back += 1
        coupon_date = maturity_date - relativedelta(months=6 * periods_back)

    coupon_dates.reverse()
    return coupon_date, coupon_dates



if __name__ == "__main__":

    maturity_date = date(2036, 5, 15)
    settlement_date = date(2035, 6, 15)

    previous_coupon_date, coupon_dates = build_coupon_schedule(maturity_date, settlement_date)
    next_coupon_date = coupon_dates[0]

    fraction_elapsed = calculate_30_360_fraction(
        previous_coupon_date, settlement_date, next_coupon_date
    )

    accrued_interest = calculate_accrued_interest(
        face_value=1000,
        coupon_rate=0.0525,
        coupon_frequency=2,
        fraction_elapsed=fraction_elapsed,
    )

    clean_price = 980.0
    dirty_price = clean_to_dirty(clean_price, accrued_interest)

    solved_yield = solve_ytm(
        face_value=1000,
        coupon_rate=0.0525,
        remaining_payments=len(coupon_dates),
        market_price=dirty_price,
        upper_yield=0.10,
        coupon_frequency=2,
        fraction_elapsed=fraction_elapsed,
    )

    repriced_dirty_price = price_bond(
        face_value=1000,
        coupon_rate=0.0525,
        remaining_payments=len(coupon_dates),
        annual_yield=solved_yield,
        coupon_frequency=2,
        fraction_elapsed=fraction_elapsed,
    )

    print(f"Yield to maturity: {solved_yield:.4%}")

    print("Next coupon date:", next_coupon_date)
    print("Fraction elapsed:", fraction_elapsed)
    print(f"Accrued interest: ${accrued_interest:.3f}")
    print(f"Dirty price: ${dirty_price:.3f}")
    print(f"Repriced dirty price: ${repriced_dirty_price:.3f}")

    for payment_date in coupon_dates:
        print(payment_date)




    print("Remaining payments:", len(coupon_dates))
    print("Previous coupon date:", previous_coupon_date)