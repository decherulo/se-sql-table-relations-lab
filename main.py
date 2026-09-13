# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

print(pd.read_sql("""SELECT * FROM sqlite_master""", conn))

# ---------------- Part 1: Join and Filter ----------------

# 1. First and last names + job titles for all employees in Boston
q1 = """
SELECT firstName, lastName, jobTitle
FROM employees
JOIN offices ON employees.officeCode = offices.officeCode
WHERE offices.city = 'Boston';
"""
print(pd.read_sql(q1, conn))

# 2. Are there any offices with zero employees?
q2 = """
SELECT offices.officeCode, offices.city, COUNT(employees.employeeNumber) AS numEmployees
FROM offices
LEFT JOIN employees ON offices.officeCode = employees.officeCode
GROUP BY offices.officeCode
HAVING COUNT(employees.employeeNumber) = 0;
"""
print(pd.read_sql(q2, conn))

# ---------------- Part 2: Type of Join ----------------

# 3. All employees' first/last name, city and state of their office (include all employees)
q3 = """
SELECT employees.firstName, employees.lastName, offices.city, offices.state
FROM employees
LEFT JOIN offices ON employees.officeCode = offices.officeCode
ORDER BY employees.firstName, employees.lastName;
"""
print(pd.read_sql(q3, conn))

# 4. Customers who have not placed an order (contact info + sales rep employee number)
q4 = """
SELECT customers.contactFirstName, customers.contactLastName, customers.phone,
       customers.salesRepEmployeeNumber
FROM customers
LEFT JOIN orders ON customers.customerNumber = orders.customerNumber
WHERE orders.orderNumber IS NULL
ORDER BY customers.contactLastName;
"""
print(pd.read_sql(q4, conn))

# ---------------- Part 3: Built-In Function ----------------

# 5. Customer contacts + payment amounts/dates, sorted by amount descending (cast amount to a number)
q5 = """
SELECT customers.contactFirstName, customers.contactLastName,
       payments.amount, payments.paymentDate
FROM customers
JOIN payments ON customers.customerNumber = payments.customerNumber
ORDER BY CAST(payments.amount AS REAL) DESC;
"""
print(pd.read_sql(q5, conn))

# ---------------- Part 4: Joining and Grouping ----------------

# 6. Employees whose customers have an average credit limit over 90k
q6 = """
SELECT employees.employeeNumber, employees.firstName, employees.lastName,
       COUNT(customers.customerNumber) AS numcustomers
FROM employees
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY employees.employeeNumber
HAVING AVG(customers.creditLimit) > 90000
ORDER BY numcustomers DESC;
"""
print(pd.read_sql(q6, conn))

# 7. Top-selling products: number of orders and total units sold
q7 = """
SELECT products.productName,
       COUNT(orderdetails.orderNumber) AS numorders,
       SUM(orderdetails.quantityOrdered) AS totalunits
FROM products
JOIN orderdetails ON products.productCode = orderdetails.productCode
GROUP BY products.productCode
ORDER BY totalunits DESC;
"""
print(pd.read_sql(q7, conn))

# ---------------- Part 5: Multiple Joins ----------------

# 8. Number of unique customers who ordered each product
q8 = """
SELECT products.productName, products.productCode,
       COUNT(DISTINCT orders.customerNumber) AS numpurchasers
FROM products
JOIN orderdetails ON products.productCode = orderdetails.productCode
JOIN orders ON orderdetails.orderNumber = orders.orderNumber
GROUP BY products.productCode
ORDER BY numpurchasers DESC;
"""
print(pd.read_sql(q8, conn))

# 9. Number of customers per office
q9 = """
SELECT offices.officeCode, offices.city,
       COUNT(customers.customerNumber) AS n_customers
FROM offices
JOIN employees ON offices.officeCode = employees.officeCode
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY offices.officeCode;
"""
print(pd.read_sql(q9, conn))

# ---------------- Part 6: Subquery ----------------

# 10. Employees who sold products ordered by fewer than 20 customers
q10 = """
SELECT DISTINCT employees.employeeNumber, employees.firstName, employees.lastName,
       offices.city, offices.officeCode
FROM employees
JOIN offices ON employees.officeCode = offices.officeCode
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
JOIN orders ON customers.customerNumber = orders.customerNumber
JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
WHERE orderdetails.productCode IN (
    SELECT orderdetails.productCode
    FROM orderdetails
    JOIN orders ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY orderdetails.productCode
    HAVING COUNT(DISTINCT orders.customerNumber) < 20
);
"""
print(pd.read_sql(q10, conn))

# 11. Close the connection
conn.close()