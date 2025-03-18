def find_emails(text):
    import re
    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    emails = re.match(email_pattern, text)
    return emails