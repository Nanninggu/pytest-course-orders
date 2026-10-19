def discount_rate(quantity: int, is_member: bool) -> int:
    """할인율(%)을 돌려준다. 회원은 5%, 10개 이상 구매는 3%를 더한다."""
    rate = 0
    if is_member:
        rate += 5
    if quantity >= 10:
        rate += 3
    return rate
