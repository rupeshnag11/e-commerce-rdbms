Schema

A schema is a namespace/container inside a database that organizes database objects such as tables, views, functions, etc.

PostgreSQL creates a default schema called:

public

So initially:

ecommerce_db
      |
      └── public
             |
             └── tables

For this learning project, we'll initially use:

public

We don't need to create multiple schemas yet.


Schema means the structure/design of a database.

In simple words:

Schema tells us what data we can store and how that data is organized.

Think of it like a blueprint of a house.
Before building a house, you decide where the bedroom, kitchen, and bathroom will be. Similarly, before storing data, we define tables, columns, relationships, constraints, etc.

E-commerce Example

Suppose we are building an e-commerce application.

Our database might have:

E-commerce Database
│
├── customers
├── products
├── orders
└── payments

The schema defines what each table looks like.

Customers table
Column	Data Type
customer_id	INTEGER
name	VARCHAR
email	VARCHAR
phone	VARCHAR
Products table
Column	Data Type
product_id	INTEGER
product_name	VARCHAR
price	DECIMAL
stock	INTEGER

This structure is part of the database schema.

Schema also defines relationships

For example:

Customer
   ↓
customer_id
   ↓
Order

One customer can have many orders.

Customer 1 ────────< Orders

The schema defines this relationship using things such as Primary Key and Foreign Key.

Schema vs Data

This is very important.

Schema = Structure
customers
----------------
customer_id
name
email
phone
Data = Actual information
1 | Rupesh | rupesh@gmail.com | 9876543210
2 | Ravi   | ravi@gmail.com   | 9123456780

So:

Schema = How data is organized

Data = Actual values stored inside that structure

Real-World Example

Think about an Excel sheet.

Before entering information, you decide:

Column A → Customer ID
Column B → Name
Column C → Email
Column D → Phone

That's similar to a schema.

Then:

1 | Rupesh | rupesh@gmail.com | 9876543210

is the data.

In PostgreSQL

You might create a table like:

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15)
);

Here you're defining the structure/schema of the customers table.

Then:

INSERT INTO customers
VALUES (1, 'Rupesh', 'rupesh@gmail.com', '9876543210');

This adds the actual data.

🧠 Beginner Memory Trick

Schema = Blueprint

Table = Room

Column = Type of information

Row = One actual record

Data = Actual values

Example:

Schema
   ↓
customers table
   ↓
columns: id, name, email
   ↓
rows: actual customers

One-line definition:

A database schema is the blueprint that defines how data is organized, including tables, columns, data types, relationships, and constraints.




Role/User

PostgreSQL uses roles for managing database access.

A role can have login capability and permissions.

For example:

postgres

is commonly created as an administrative role during installation.

Later we can create a dedicated application role such as:

ecommerce_app

Conceptually:

postgres
   |
   +-- administer database
   |
   +-- create users
   |
   +-- manage permissions

ecommerce_app
   |
   +-- application access
   |
   +-- limited permissions

Important production principle:

Don't let your application connect using a superuser in a real production environment.

We'll learn proper permissions later.

7. Install PostgreSQL

Because you're on Windows, the normal setup is:

Install PostgreSQL.
Set the PostgreSQL administrator password.
Keep the default port unless you have a reason to change it.
Install pgAdmin if offered.
Verify that PostgreSQL is running.

The standard PostgreSQL port is:

5432

So conceptually:

localhost:5432

means:

PostgreSQL server running on this computer at port 5432.

8. Verify PostgreSQL

Open PowerShell or Command Prompt:

psql --version

You should get something similar to:

psql (PostgreSQL 17.x)

The exact version can differ.

Then:

psql -U postgres

It may ask for the password you created during installation.

If successful, you'll see something similar to:

postgres=#

That means:

You are now inside PostgreSQL's command-line interface.

9. What is psql?

This is important.

psql is not PostgreSQL itself.

It is a command-line client used to interact with PostgreSQL.

Think:

PostgreSQL
    ↑
    |
  psql
    ↑
    |
   You

You type:

SELECT version();

and PostgreSQL returns information about the server.




1. File System — simple example

Imagine an e-commerce company stores customer information in files:

customers.txt
orders.txt
payments.txt
products.txt

Suppose customer Ravi places an order.

customers.txt

101, Ravi, 9876543210, Hyderabad

orders.txt

5001, Ravi, Laptop, 60000

payments.txt

5001, Ravi, 60000, Paid
Problem

Ravi changes his phone number.

You now have to find every file containing Ravi's phone number and update it.

If you update customers.txt but forget another file:

customers.txt → 9999999999
orders.txt    → 9876543210

Now the same customer has two different phone numbers.

That's data inconsistency.

2. Database System — same example

Instead of keeping separate independent files, we use PostgreSQL.

We can have related tables:

customers
---------
customer_id
name
phone

orders
---------
order_id
customer_id
product_id

products
---------
product_id
name
price

payments
---------
payment_id
order_id
amount
status

For example:

customers
101 | Ravi | 9876543210

orders
5001 | 101 | 201

products
201 | Laptop | 60000

payments
9001 | 5001 | 60000 | Paid

The important thing is that the tables are related using IDs.

If Ravi changes his phone number:

UPDATE customers
SET phone = '9999999999'
WHERE customer_id = 101;

We update it once.

3. Now understand each disadvantage with the same example
File System Problem	Database Solution	Simple Example
Data redundancy	Reduces duplication	Ravi's details don't need to be copied everywhere
Data inconsistency	Centralized data	Change Ravi's phone once
Difficult data access	SQL queries	SELECT * FROM customers WHERE name='Ravi';
Data isolation	Related tables	Customer → Order → Payment can be connected
Integrity problems	Constraints	Order cannot reference a non-existing customer
Atomicity problems	Transactions	Payment + order can succeed together or fail together
Concurrent access problems	Concurrency control	2 users buying the last product won't incorrectly both get it
Security problems	Roles & permissions	Customer can see their orders but cannot modify payment records
4. Atomicity — very important example

Suppose Ravi buys a laptop for ₹60,000.

The system needs to do:

1. Create Order
2. Deduct ₹60,000
3. Reduce Laptop stock
4. Record Payment

Imagine step 1 and 2 succeed, but step 3 fails.

File System

You might end up with:

Order      → Created ✅
Payment    → ₹60,000 deducted ✅
Stock      → Not updated ❌

Now the system is inconsistent.

Database

A database uses a transaction:

BEGIN

Create Order
Deduct Payment
Reduce Stock
Record Payment

COMMIT

If something fails:

ROLLBACK

Everything is undone.

So:

Either all operations happen, or none of them happen.

That's Atomicity.

5. Concurrent Access — simple example

Suppose there is only 1 iPhone left.

Two customers click Buy at almost the same time:

Ravi       → Buy iPhone
Suresh     → Buy iPhone
Without proper database control

Both might see:

Stock = 1

Both purchase it.

Result:

Stock = -1 ❌
Database

The DBMS manages concurrent transactions so that only one transaction can successfully update the remaining stock.

Result:

Ravi       → Order successful ✅
Suresh     → Out of stock ❌
6. Security — simple example

In a file system, you might have:

payments.txt

If someone gets permission to that file, they may potentially access all payment information.

In PostgreSQL, you can create roles:

Customer
   ↓
Can view own orders

Support Staff
   ↓
Can view customer/order information

Admin
   ↓
Can manage everything

This gives much finer control.

Final understanding

Think of it this way:

File System
Application
    ↓
Files
    ↓
customers.txt
orders.txt
payments.txt
products.txt

The application itself has to handle much of the logic for relationships, consistency, transactions, etc.

Database System
Application
      ↓
     DBMS
      ↓
PostgreSQL Database
      ↓
Customers ↔ Orders ↔ Products ↔ Payments

The DBMS takes responsibility for managing the data safely and efficiently.

One-line interview answer

A file system mainly manages files, whereas a database system manages structured, related data and provides features such as SQL querying, integrity, transactions, concurrency control, and security.

Easy memory trick:

File System = Store files
Database System = Store + relate + protect + query + control data