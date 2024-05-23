def clear_phone_number(phone):
    if phone:
        phone = str(phone).strip().replace("-", "").replace("(", "").replace(")", "")
        phone = "+" + phone if phone[0] != "+" else phone

    return phone
