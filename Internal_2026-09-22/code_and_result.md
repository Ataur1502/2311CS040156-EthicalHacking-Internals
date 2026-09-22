# Code and Result Document

Name: Ataur  
Roll number: 2311CS040156  
Date: 2026-09-22

This document contains safe local demonstration code and results for the assigned internal questions. The output represents controlled local simulations, not testing of any live or external target.

## Question 5 SQL Injection Detection and Prevention

### Code

```python
import sqlite3

def setup_database():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.executemany(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        [
            ("admin", "admin123"),
            ("student", "student@123"),
        ],
    )
    connection.commit()
    return connection

def vulnerable_login(connection, username, password):
    query = (
        "SELECT username FROM users WHERE username = '"
        + username
        + "' AND password = '"
        + password
        + "'"
    )
    rows = connection.execute(query).fetchall()
    return query, rows

def safe_login(connection, username, password):
    query = "SELECT username FROM users WHERE username = ? AND password = ?"
    rows = connection.execute(query, (username, password)).fetchall()
    return query, rows

if __name__ == "__main__":
    database = setup_database()
    payload_username = "' OR '1'='1' -- "
    payload_password = "anything"

    vulnerable_query, vulnerable_rows = vulnerable_login(database, payload_username, payload_password)
    safe_query, safe_rows = safe_login(database, payload_username, payload_password)

    print("SQL Injection Detection and Prevention Demo")
    print("Payload username:", payload_username)
    print("Vulnerable query:", vulnerable_query)
    print("Vulnerable result:", vulnerable_rows)
    print("Safe query:", safe_query)
    print("Safe result:", safe_rows)
```

### Result

```text
SQL Injection Detection and Prevention Demo
Payload username: ' OR '1'='1' --
Vulnerable query: SELECT username FROM users WHERE username = '' OR '1'='1' -- ' AND password = 'anything'
Vulnerable result: [('admin',), ('student',)]
Safe query: SELECT username FROM users WHERE username = ? AND password = ?
Safe result: []
```

### Interpretation

The vulnerable query joined user input directly into SQL, so the payload changed the query logic. The safe query used placeholders, so the database treated the payload as text and did not return unauthorized rows.

## Question 7 Password Security and Authentication Testing

### Code

```python
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
```

### Result

```text
Password Security and Authentication Testing Demo
admin {'minimum_length': False, 'uppercase': False, 'lowercase': True, 'digit': False, 'special_character': False} FAIL
password123 {'minimum_length': True, 'uppercase': False, 'lowercase': True, 'digit': True, 'special_character': False} FAIL
Student@2026 {'minimum_length': True, 'uppercase': True, 'lowercase': True, 'digit': True, 'special_character': True} PASS
Salt length: 16
Hash length: 32
Correct password verification: True
Wrong password verification: False
Lockout result: Account locked after repeated failed attempts
```

### Interpretation

The weak passwords failed because they did not satisfy the full policy. The strong password passed and was stored as a salted PBKDF2 hash. Verification succeeded only for the correct password, and the lockout simulation blocked repeated failed attempts.
