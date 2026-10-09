"""Tiny demo service used to test the Bob the Fixer GitHub App."""


def get_user_email(users: dict, user_id: str) -> str:
    user = users.get(user_id)
    if user is None:
        return ""
    return user["email"]


def greet(name: str) -> str:
    return f"Hello, {name}!"
