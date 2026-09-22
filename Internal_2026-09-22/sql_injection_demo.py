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
