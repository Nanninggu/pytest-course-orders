# 2019년에 급하게 만든 배송비 계산입니다. 테스트가 없고, 왜 이렇게 짰는지 아는 사람도 없습니다.
def calc_shipping(weight, country, express=False, coupon=None):
    fee = 0
    if country == "KR":
        if weight <= 1:
            fee = 3000
        elif weight <= 5:
            fee = 5000
        else:
            fee = 5000 + int((weight - 5) * 800)
    elif country == "US" or country == "CA":
        fee = 15000 + int(weight * 2000)
        if weight > 20:
            fee = fee * 1.1
    else:
        fee = 25000
    if express:
        fee = fee * 2
    return _apply_coupon(fee, coupon)


def _apply_coupon(fee, coupon):
    if coupon == "FREE":
        return 0
    if coupon == "HALF":
        return fee / 2
    return fee
