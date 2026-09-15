# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

print(pd.read_sql("""SELECT * FROM sqlite_master""", conn))


# ===== Part 1: Join and Filter =====

# Q1: Boston employees
q1 = pd.read_sql("""
SELECT firstName, lastName, jobTitle
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
WHERE o.city = 'Boston'
""", conn)
print("Q1:\n", q1, "\n")

# Q2: Offices with zero employees
q2 = pd.read_sql("""
SELECT o.officeCode, o.city
FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode
WHERE e.employeeNumber IS NULL
""", conn)
print("Q2:\n", q2, "\n")


# ===== Part 2: Type of Join =====

# Q3: All employees + office city/state
q3 = pd.read_sql("""
SELECT e.firstName, e.lastName, o.city, o.state
FROM employees e
LEFT JOIN offices o ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName
""", conn)
print("Q3:\n", q3, "\n")

# Q4: Customers with no orders (should be 24 rows)
q4 = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName
""", conn)
print("Q4:\n", q4, "\n")


# ===== Part 3: Built-In Function =====

# Q5: Customer payments, sorted by amount (CAST needed)
q5 = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
FROM customers c
JOIN payments p ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC
""", conn)
print("Q5:\n", q5, "\n")


# ===== Part 4: Joining and Grouping =====

# Q6: Reps with avg customer credit limit > 90k (should be 4 people)
q6 = pd.read_sql("""
SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS numcustomers
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
HAVING AVG(CAST(c.creditLimit AS REAL)) > 90000
ORDER BY numcustomers DESC
""", conn)
print("Q6:\n", q6, "\n")

# Q7: Product order counts + total units sold
q7 = pd.read_sql("""
SELECT p.productName,
       COUNT(od.orderNumber) AS numorders,
       SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName
ORDER BY totalunits DESC
""", conn)
print("Q7:\n", q7, "\n")


# ===== Part 5: Multiple Joins =====

# Q8: Product + distinct purchaser count
q8 = pd.read_sql("""
SELECT p.productName, p.productCode,
       COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY numpurchasers DESC
""", conn)
print("Q8:\n", q8, "\n")

# Q9: Customers per office
q9 = pd.read_sql("""
SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
""", conn)
print("Q9:\n", q9, "\n")


# ===== Part 6: Subquery =====

# Q10: Employees who sold products ordered by fewer than 20 customers
q10 = pd.read_sql("""
SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord ON c.customerNumber = ord.customerNumber
JOIN orderdetails od ON ord.orderNumber = od.orderNumber
WHERE od.productCode IN (
    SELECT od2.productCode
    FROM orderdetails od2
    JOIN orders ord2 ON od2.orderNumber = ord2.orderNumber
    GROUP BY od2.productCode
    HAVING COUNT(DISTINCT ord2.customerNumber) < 20
)
""", conn)
print("Q10:\n", q10, "\n")


# Q11: Close the connection
conn.close()