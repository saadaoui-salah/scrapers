def find_emails(text):
    import re
    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    emails = re.search(email_pattern, text)
    if not emails:
        return []
    print(emails)
    return emails.group()