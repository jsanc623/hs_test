import os


def builder(uri='dataset'):
    user_key = os.getenv('USER_KEY')
    base_url = os.getenv('BASE_URL')
    parts = [base_url, uri, f"?userKey={user_key}"]
    return '/'.join(parts)
