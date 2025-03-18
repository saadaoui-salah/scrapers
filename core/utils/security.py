def decode_cf_email(cf_email):
    r = int(cf_email[:2], 16)
    email = ''.join(chr(int(cf_email[i:i+2], 16) ^ r) for i in range(2, len(cf_email), 2))
    return email
