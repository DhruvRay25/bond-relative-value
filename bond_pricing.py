def price_bond(face_value, coupon_rate, remaining_payments, annual_yield, coupon_frequency=1, fraction_elapsed=0.0):

    coupon_payment = (face_value*coupon_rate)/coupon_frequency
    total_periods = remaining_payments
    period_yield = (annual_yield/coupon_frequency)

   

    #print("Annual Coupon", annual_coupon)

    bond_price = 0

    for period in range(1, total_periods + 1):
        
        cash_flow = coupon_payment

        if period == total_periods:
            cash_flow += face_value

        periods_until_payment = period - fraction_elapsed
        present_value = cash_flow/(1+period_yield)**(periods_until_payment)
        bond_price += present_value

        #print(f"Year {year}: ${cash_flow:.2f}, PV ${present_value:.2f}")

    #print(f"Bond Price: ${bond_price:.2f}") 

    
    return(bond_price)

if __name__ == "__main__":
    calculated_price = price_bond(
        face_value=1000,
        coupon_rate=0.05,
        remaining_payments=3,
        annual_yield=0.06,
    )
    semiannual_price=price_bond(
        face_value=1000,
        coupon_rate=0.05,
        remaining_payments=3, 
        annual_yield=0.05, 
        coupon_frequency=2
    )
    print(f"Semiannual bond price: ${semiannual_price:.2f}")
    print(f"Bond price: ${calculated_price:.2f}")

    three_payment_price = price_bond(
        face_value=1000,
        coupon_rate=0.06,
        remaining_payments=3,
        annual_yield=0.06,
        coupon_frequency=2,
        fraction_elapsed=0.5
    )

    expected_price = (30 / (1.03 ** 0.5)) + (30 / (1.03 ** 1.5)) + (1030 / (1.03 ** 2.5))

    print(f"Three-payment price: ${three_payment_price:.6f}")
    print(f"Expected price: ${expected_price:.6f}")


yields_to_compare = [0.04, 0.05, 0.06]

for annual_yield in yields_to_compare:
    calculated_price = price_bond(
        face_value=1000, 
        coupon_rate=0.05,
        remaining_payments=3, 
        annual_yield=annual_yield, 
    )
    #print(f"Yield: {annual_yield:.1%} | Price: ${calculated_price:.2f}")


semiannual_price = price_bond(
    face_value=1000,
    coupon_rate=0.05, 
    remaining_payments=3, 
    annual_yield=0.05, 
    coupon_frequency=2
)