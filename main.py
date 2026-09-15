# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

print(pd.read_sql("""SELECT * FROM sqlite_master""", conn))


# ===== Part 1: Join and Filter =====

# df_boston: Boston employees
df_boston = pd.read_sql("""
SELECT firstName, lastName
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
WHERE o.city = 'Boston'
""", conn)
print("df_boston:\n", df_boston, "\n")

# df_zero_emp: Offices with zero employees
df_zero_emp = pd.read_sql("""
SELECT o.officeCode, o.city
FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode
WHERE e.employeeNumber IS NULL
""", conn)
print("df_zero_emp:\n", df_zero_emp, "\n")


# ===== Part 2: Type of Join =====

# df_employee: All employees + office city/state
df_employee = pd.read_sql("""
SELECT e.firstName, e.lastName, o.city, o.state
FROM employees e
LEFT JOIN offices o ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName
""", conn)
print("df_employee:\n", df_employee, "\n")

# df_contacts: Customers with no orders
df_contacts = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName
""", conn)
print("df_contacts:\n", df_contacts, "\n")


# ===== Part 3: Built-In Function =====

# df_payment: Customer payments, sorted by amount
df_payment = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
FROM customers c
JOIN payments p ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC
""", conn)
print("df_payment:\n", df_payment, "\n")


# ===== Part 4: Joining and Grouping =====

# df_credit: Reps with avg customer credit limit > 90k
df_credit = pd.read_sql("""
SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS numcustomers
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
HAVING AVG(CAST(c.creditLimit AS REAL)) > 90000
ORDER BY numcustomers DESC
""", conn)
print("df_credit:\n", df_credit, "\n")

# df_product_sold: Product order counts + total units sold
df_product_sold = pd.read_sql("""
SELECT p.productName,
       COUNT(od.orderNumber) AS numorders,
       SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName
ORDER BY totalunits DESC
""", conn)
print("df_product_sold:\n", df_product_sold, "\n")


# ===== Part 5: Multiple Joins =====

# df_total_customers: Product + distinct purchaser count
df_total_customers = pd.read_sql("""
SELECT p.productName, p.productCode,
       COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY numpurchasers DESC
""", conn)
print("df_total_customers:\n", df_total_customers, "\n")

# df_customers: Customers per office
df_customers = pd.read_sql("""
SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
""", conn)
print("df_customers:\n", df_customers, "\n")


# ===== Part 6: Subquery =====

# df_under_20: Employees who sold products ordered by fewer than 20 customers
df_under_20 = pd.read_sql("""
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
print("df_under_20:\n", df_under_20, "\n")


# Close the connection
conn.close()