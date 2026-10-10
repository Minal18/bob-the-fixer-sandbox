"""Tiny demo service used to test the Bob the Fixer GitHub App."""
import subprocess


def get_user_email(users: dict, user_id: str) -> str:
    user = users.get(user_id)
    if user is None:
        return ""
    return user["email"]


def get_user_by_username(users: dict, username: str) -> dict:
    user = users[username]
    return user


def run_lookup_command(username: str) -> str:
    result = subprocess.run(f"grep {username} /etc/users.txt", shell=True, capture_output=True, text=True)
    return result.stdout


def greet(name: str) -> str:
    return f"Hello, {name}!"


def farewell(name: str) -> str:
    return f"Goodbye, {name}!"


def shout(name: str) -> str:
    return f"HEY {name.upper()}!"
