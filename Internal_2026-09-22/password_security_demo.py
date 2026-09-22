import hashlib
import hmac
import os
import re


ITERATIONS = 200_000


def check_password_policy(password):
    checks = {
        "minimum_length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "special_character": bool(re.search(r"[^A-Za-z0-9]", password)),
    }
    return checks


def policy_passed(checks):
    return all(checks.values())


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
    )
    return salt, password_hash


def verify_password(password, salt, expected_hash):
    _, calculated_hash = hash_password(password, salt)
    return hmac.compare_digest(calculated_hash, expected_hash)


def simulate_lockout(attempts, max_attempts=3):
    failed_attempts = 0
    for attempt in attempts:
        if attempt:
            return "Login successful"
        failed_attempts += 1
        if failed_attempts >= max_attempts:
            return "Account locked after repeated failed attempts"
    return "Login failed"


if __name__ == "__main__":
    samples = ["admin", "password123", "Student@2026"]
    print("Password Security and Authentication Testing Demo")
    for sample in samples:
        checks = check_password_policy(sample)
        print(sample, checks, "PASS" if policy_passed(checks) else "FAIL")

    salt, stored_hash = hash_password("Student@2026")
    print("Salt length:", len(salt))
    print("Hash length:", len(stored_hash))
    print("Correct password verification:", verify_password("Student@2026", salt, stored_hash))
    print("Wrong password verification:", verify_password("wrongpass", salt, stored_hash))
    print("Lockout result:", simulate_lockout([False, False, False]))

