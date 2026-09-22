# Ethical Hacking Internal Report

Name: Ataur  
Roll number: 2311CS040156  
Date: 2026-09-22

## Question 5 SQL Injection Detection and Prevention

### Aim

To understand how SQL injection happens when untrusted input is directly joined into a database query, and to show how input validation and parameterized queries prevent it.

### Key concepts

SQL injection is a web application weakness where user input is interpreted as part of an SQL command. It can allow an attacker to bypass authentication, read unintended records, modify data, or delete data. Detection usually involves checking whether special SQL characters or boolean payloads change the behavior of a form. Prevention depends on parameterized queries, input validation, least privilege database accounts, and safe error handling.

### Lab target

Suggested target: DVWA.  
Submission method used here: safe local simulation using the same idea as a vulnerable login or search form. No external target was tested.

### Process

1. A sample user table was considered with normal records such as admin and student.
2. A vulnerable query pattern was reviewed where the application builds a query by directly adding user input into the SQL string.
3. A test input such as `' OR '1'='1' --` was used in the simulation to represent the injection attempt.
4. The same input was then checked with a parameterized query, where the input is treated as data only.
5. Basic input validation and error handling practices were noted as additional controls.

### Result

The vulnerable query treated the injected condition as SQL logic and returned a successful match in the simulated test. The parameterized query treated the same payload as ordinary text and returned no unauthorized match. This shows that parameterized queries are the main defense against SQL injection, while validation and least privilege reduce additional risk.

### Prevention points

- Use parameterized queries or prepared statements for every database operation.
- Validate input length, type, and expected format before processing it.
- Avoid displaying raw SQL errors to users.
- Use a database account with only the permissions required by the application.
- Log suspicious inputs for review.

## Question 7 Password Security and Authentication Testing

### Aim

To study password policy weaknesses, secure password storage, salting, hashing, and common authentication risks.

### Key concepts

Password security depends on both user password strength and server-side storage. Weak passwords can be guessed easily, and plain text password storage can expose all accounts if the database is leaked. Secure systems store salted password hashes using slow hashing functions. Authentication testing checks password policy, login error messages, account lockout, session handling, and resistance to brute-force attempts.

### Lab target

Suggested target: local test application.  
Submission method used here: safe local simulation of password validation, salted hashing, and login lockout logic.

### Process

1. Several sample passwords were checked against a basic password policy.
2. The policy checked minimum length, uppercase letters, lowercase letters, digits, and special characters.
3. A strong password was converted into a salted hash using a slow key derivation function.
4. A login verification step compared the submitted password hash with the stored hash.
5. Repeated failed login attempts were simulated to demonstrate account lockout behavior.

### Result

Weak passwords failed the policy checks because they were short or lacked character variety. The strong password passed the policy check and was stored as a salted hash instead of plain text. During authentication, the correct password verified successfully, while incorrect attempts failed. After repeated failures, the account was locked in the simulation. This shows that secure authentication requires strong password rules, salted slow hashing, generic error messages, and rate limiting or lockout controls.

### Prevention points

- Never store passwords in plain text.
- Use a unique salt for every password.
- Use slow password hashing such as PBKDF2, bcrypt, scrypt, or Argon2.
- Apply rate limiting or temporary lockout after repeated failed attempts.
- Use generic login errors such as "Invalid username or password".
- Enable multi-factor authentication where possible.

## Conclusion

SQL injection and weak authentication are common application security risks. SQL injection is prevented mainly by parameterized queries and careful input handling. Password attacks are reduced by strong password policies, salted slow hashing, and login protection controls. The simulations show the difference between unsafe and safe implementation patterns without testing any real external system.
