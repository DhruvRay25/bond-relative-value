from bond_pricing import price_bond

def solve_ytm(face_value, coupon_rate, remaining_payments, market_price, lower_yield=0.04, upper_yield=0.08, coupon_frequency=1, fraction_elapsed=0.0):
    
    price_tolerance = 0.000001

    price_at_lower = price_bond(face_value, coupon_rate, remaining_payments, lower_yield, coupon_frequency=coupon_frequency, fraction_elapsed=fraction_elapsed)
    price_at_upper = price_bond(face_value, coupon_rate, remaining_payments, upper_yield, coupon_frequency=coupon_frequency, fraction_elapsed=fraction_elapsed)

    if not (price_at_upper <= market_price <= price_at_lower):
        raise ValueError("Market price is outside the supplied yield range.")

    for attempt in range(100):
        trial_yield = (lower_yield+upper_yield)/2
        #print(f"Attempt {attempt + 1}: yield {trial_yield:.3%}")

        trial_price = price_bond(face_value, coupon_rate, remaining_payments, trial_yield, coupon_frequency=coupon_frequency, fraction_elapsed=fraction_elapsed)

        price_error = trial_price - market_price
        if abs(price_error) < price_tolerance:
            return trial_yield
        #print(f"Pricing error: ${price_error:.2f}")


            

        if price_error > 0:
            lower_yield = trial_yield

        elif price_error < 0:
            upper_yield = trial_yield

    raise RuntimeError("Yield Search did not converge within 100 Attempts")

if __name__ == "__main__":

    semiannual_market_price = price_bond(
        face_value=1000,
        coupon_rate=0.05, 
        years_to_maturity=3, 
        annual_yield=0.065, 
        coupon_frequency=2
    )

    semiannual_solved_yield = solve_ytm(
        face_value=1000,
        coupon_rate=0.05, 
        years_to_maturity=3,
        market_price=semiannual_market_price, 
        coupon_frequency=2
    )

    print(f"Semiannual price: ${semiannual_market_price:.2f}")
    print(f"Recovered YTM: {semiannual_solved_yield:.6%}")

    solved_yield = solve_ytm(1000, 0.05, 10, 950)
    print(f"Solved YTM: {solved_yield:.4%}")

    recalculated_price = price_bond(1000, 0.05, 10, solved_yield)
    print(f"Recalculated price: ${recalculated_price:.6f}")

    assert (abs(semiannual_solved_yield-0.065) < 0.00000001)


    



