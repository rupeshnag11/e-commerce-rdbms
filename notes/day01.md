https://rdbms-resource-pack-650qinf.gamma.site/

| Problem | Description |
| --- | --- |
| Data Redundancy | Same data stored multiple times |
| Data Inconsistency | Different copies contain different values |
| Data Isolation | Data scattered across many files |
| Difficult Search | Large files require slow searches |
| Poor Security | Limited access control |
| No Transactions | Updates can be incomplete or conflicting |
| Concurrency Issues | Simultaneous updates may overwrite each other |
| Backup Difficulty | Recovery is challenging |
| Data Dependency | Programs break when file formats change |

# 1. What is Data?

**Data is raw facts or values that have not yet been processed or interpreted.**

Data by itself may not give us a clear meaning.

### Example

Suppose we have these marks:

```
75, 82, 60, 90, 45
```

These are **data**.

We only have numbers. We don't yet know:

- Who scored them?
- Who got the highest mark?
- What is the average?
- How many students passed?

So, this is **raw data**.

### Simple definition

> **Data = Raw facts and values**
> 

---

# 2. Types of Data

There are two basic types:

## A. Quantitative Data

**Quantitative data is numerical data that can be counted or measured.**

Examples:

```
Age = 25
Salary = ₹50,000
Weight = 70 kg
Height = 175 cm
Number of students = 50
```

### Easy way to remember

> **Quantitative = Quantity = Numbers**
> 

---

## B. Qualitative Data

**Qualitative data describes characteristics or qualities and is generally non-numerical.**

Examples:

```
Name = Rupesh
Hair Color = Black
City = Vijayawada
Gender = Male
Product Color = Red
```

### Easy way to remember

> **Qualitative = Quality = Description**
> 

---

# 3. What is Information?

**Information is data that has been processed and organized so that it becomes meaningful and useful.**

### Example

Raw data:

```
75, 82, 60, 90, 45
```

After processing:

```
Average mark = 70.4
Highest mark = 90
Lowest mark = 45
```

Now the numbers have meaning.

This is **information**.

### Simple definition

> **Information = Processed and meaningful data**
> 

---

# 4. Data vs Information

Let's understand with a real-life example.

Imagine a shop has this data:

```
Product       Sales
Laptop        10
Mobile        50
Headphones    30
Keyboard      20
```

This is **data**.

After analyzing it:

```
Mobile is the best-selling product.
50 mobiles were sold.
Mobile sales are higher than laptop sales.
```

This is **information**.

The information can help the shop owner decide:

> "I should keep more mobile phones in stock."
> 

So:

**Data → Processing/Analysis → Information → Decision**

---

# 5. Very Simple Example

Think about **student marks**.

### Data

```
Student     Marks
Ravi        80
Ram         45
Sita        90
John        35
```

These are raw facts → **DATA**

### Processing

We calculate:

```
Highest mark = 90
Lowest mark = 35
Average = 62.5
```

These results → **INFORMATION**

### Decision

Teacher concludes:

> "Sita performed the best, while John needs improvement."
> 

That conclusion helps in **decision-making**.

---

# 6. Data → Information

You can remember this simple flow:

```
              RAW DATA
                  ↓
          Processing / Analysis
                  ↓
             INFORMATION
                  ↓
          Decision Making
```

### Example

```
Data:
80, 90, 70, 40, 30

        ↓ Analysis

Information:
Average = 62
Highest = 90
Lowest = 30
2 students scored below 50

        ↓

Decision:
Provide additional coaching to weak students.
```

---

RDBMS

## 1. What is a Database?

A **database is an organized place where data is stored so that it can be easily accessed, updated, and managed.**

### Simple example

Imagine an online shopping application.

It needs to store:

- Customer details
- Products
- Orders
- Payments
- Addresses

All this information can be stored in a **database**.

Think of a database like a **well-organized digital cupboard**.

> **Database = Where the data is stored**
> 

---

# 2. What is DBMS?

**DBMS (Database Management System)** is the **software used to create, store, read, update, delete, secure, and manage data in a database.**

Examples:

- PostgreSQL
- MySQL
- Oracle Database
- Microsoft SQL Server

Think of it this way:

> **Database = Data storage**
> 
> 
> **DBMS = Software that manages that storage**
> 

### Real-world analogy

Think about a library.

| Real World | Database |
| --- | --- |
| Books | Data |
| Library shelves | Database |
| Librarian/system managing books | DBMS |
| Person requesting a book | Application/User |
| Book request | Query |

You don't normally walk into the storage system and manually search every book. You ask the librarian.

Similarly, an application doesn't directly manage database files. It communicates with the **DBMS**.

---

# 3. How Application, DBMS and Database Work Together

The basic flow is:

**User → Application → API → DBMS → Database**

And the response comes back:

**Database → DBMS → API → Application → User**

### Example: Shopping application

Suppose you open Amazon-like application and search:

> "Show me all laptops under ₹50,000."
> 

The flow is:

1. You enter the search in the application.
2. Application sends a request to the backend API.
3. Backend sends a SQL query to the DBMS.
4. DBMS processes the query.
5. DBMS retrieves matching data from the database.
6. Results are returned to the application.
7. Application displays the laptops to you.

For example, the backend might send:

```
SELECT*FROM productsWHERE category='Laptop'AND price<50000;
```

### Important distinction

The **API is not the database** and the **DBMS is not the application**.

Each has a different responsibility:

**Application → asks for data**

**API → carries the request**

**DBMS → manages and processes the database request**

**Database → stores the data**

---

# 4. What Does a DBMS Actually Do?

A DBMS mainly allows us to perform operations such as:

### Create

Add new data.

```powershell
INSERT INTO customers ...
```

### Read

Retrieve data.

```
SELECT*FROM customers;
```

### Update

Modify existing data.

```
UPDATE customers ...
```

### Delete

Remove data.

```
DELETEFROM customers ...
```

This is commonly called **CRUD**:

> **C = Create**
> 
> 
> **R = Read**
> 
> **U = Update**
> 
> **D = Delete**
> 

---

# 5. Why Do We Need a DBMS?

Imagine storing an e-commerce company's data in thousands of Excel files.

You would quickly face problems:

- Duplicate data
- Difficult searching
- Multiple people changing the same data
- Security problems
- Data corruption
- Difficult backup
- Difficult relationships between data
- Poor performance with large data

A DBMS solves these problems.

---

# 6. Important Characteristics of DBMS

A good DBMS provides:

### 1. Data Organization

Data can be organized into structures such as:

- Tables
- Schemas
- Views

For example:

```
customers
products
orders
payments
```

### 2. Data Security

It controls:

> **Who can access what data and what they are allowed to do.**
> 

For example:

A customer can see their own orders.

An admin may be allowed to see all orders.

---

### 3. Data Integrity

**Data integrity means keeping data accurate and reliable.**

For example:

An order should not refer to a customer that doesn't exist.

A customer's email might need to be unique.

The database can enforce these rules using constraints.

---

### 4. Concurrent Access

Multiple users can access the database at the same time.

For example:

```
User A → checking product
User B → placing order
User C → updating address
User D → checking payment
```

The DBMS manages these simultaneous operations so that data doesn't become inconsistent.

---

### 5. Backup and Recovery

If the system crashes, the DBMS provides mechanisms to recover data.

For example:

```
Database
    ↓
System crashes
    ↓
Recovery
    ↓
Data restored
```

---

# 7. ACID Properties

This is one of the **most important DBMS concepts for interviews and real backend development.**

ACID helps ensure that database transactions are reliable.

> **A = Atomicity**
> 
> 
> **C = Consistency**
> 
> **I = Isolation**
> 
> **D = Durability**
> 

Let's use a **bank transfer** example.

Suppose:

**Rupesh → transfers ₹1,000 → another account**

There are two important operations:

```
1. Deduct ₹1,000 from Rupesh
2. Add ₹1,000 to the receiver
```

## A — Atomicity

**Either everything happens, or nothing happens.**

If ₹1,000 is deducted from Rupesh but the receiver doesn't get it, that is a problem.

Atomicity ensures:

```
Deduct ₹1,000
       +
Add ₹1,000
       ↓
Both succeed → COMMIT
```

If something fails:

```
Something fails
       ↓
ROLLBACK
       ↓
No partial transaction
```

### Remember:

> **Atomicity = All or Nothing**
> 

---

## C — Consistency

### Consistency = "Data must remain correct"

The database must always follow its **rules and constraints** before and after a transaction.

**E-commerce example:**

Suppose:

```
iPhone stock = 1
```

Two customers cannot successfully buy the same single iPhone.

A valid result is:

```
Stock = 0
Customer A = Order Successful
Customer B = Out of Stock
```

An invalid result would be:

```
Stock = -1
Customer A = Successful
Customer B = Successful
```

So:

> **Consistency protects the correctness of the data.**
> 

---

## I — Isolation

**Isolation** means when multiple customers perform transactions at the same time, one transaction should **not interfere with another transaction**.

### Example: Last iPhone

Suppose:

```
iPhone stock = 1
```

Two customers buy it at the **same time**:

```
Customer A → Buy iPhone
Customer B → Buy iPhone
```

The database uses **Isolation** to coordinate these transactions.

### What should happen?

```
Customer A → Order Successful ✅
Customer B → Out of Stock ❌
Stock → 0
```

Customer B should not see or use the intermediate changes made by Customer A incorrectly.

### Without proper Isolation

Both transactions might read:

```
Stock = 1
```

and both try to purchase the same iPhone, causing incorrect inventory/order data.

### Simple definition

> **Isolation = Concurrent transactions should behave safely as if they are not interfering with each other.**
> 

**Memory trick:**

👉 **Isolation = "My transaction should not get disturbed by another transaction."**

---

## D — Durability

Once a transaction is successfully committed, the result should remain saved even if the system crashes.

Example:

```
Transfer ₹1,000
       ↓
COMMIT
       ↓
Power failure
       ↓
Database starts again
       ↓
Transfer still exists
```

### Remember:

> **Durability = Committed data stays saved**
> 

---

# 8. Applications of DBMS

DBMS is used almost everywhere.

| Industry | Example |
| --- | --- |
| Banking | Accounts, transactions, loans |
| University | Students, courses, marks |
| Railway | Trains, seats, reservations |
| Airlines | Flights, passengers, bookings |
| Telecom | Calls, customers, bills |
| Finance | Transactions and financial records |
| E-commerce | Customers, products, orders |

The common idea is:

> **Whenever an application needs to store and manage a large amount of structured data, a database is usually involved.**
> 

---

# 9. Major Advantages of DBMS

### Data Independence

Applications don't need to know exactly **how the database physically stores the data**.

For example, the DBMS can change its storage mechanism while keeping the application's database access largely unchanged.

---

### Efficient Data Access

DBMS provides mechanisms such as:

- Indexing
- Query optimization
- Caching

For example, an index can make searching for a customer by email much faster than checking every customer row.

---

### Data Integrity

The database can enforce rules such as:

```
Email must be unique
Order must belong to an existing customer
Price cannot be negative
```

---

### Concurrent Access

Many users/applications can work with the database simultaneously.

---

### Security

DBMS can control:

```
Who can access data?
What can they read?
What can they modify?
What can they delete?
```

---

### Backup & Recovery

DBMS systems provide mechanisms that help protect data from:

- Hardware failures
- Software failures
- Accidental changes
- System crashes

---

### Reduced Redundancy

**Redundancy means unnecessarily storing the same data multiple times.**

Bad design:

```
Order 101 → Rupesh, Hyderabad, 9876...
Order 102 → Rupesh, Hyderabad, 9876...
Order 103 → Rupesh, Hyderabad, 9876...
```

Better database design can separate customer information from order information and connect them using relationships.

This reduces unnecessary duplication and makes updates easier.

---

# 10. Disadvantages of DBMS

DBMS is powerful, but it also has costs.

### 1. Cost

Large database systems may require significant:

- Hardware
- Memory
- Storage
- Administration

### 2. Complexity

A production database requires knowledge of:

- SQL
- Database design
- Security
- Backup
- Performance
- Transactions
- Recovery

### 3. Resource Usage

A DBMS requires CPU, RAM, disk/storage, and other system resources.

### 4. Failure Impact

If a critical database becomes unavailable, many parts of an application may stop working.

That's why production systems use techniques such as:

- Backups
- Replication
- Failover
- Disaster recovery

# 11. SQL

SQL = **Structured Query Language**

SQL is how we communicate with PostgreSQL.

For example:

```
SELECT*FROM users;
```

Meaning:

> Give me all users.
> 

Another:

```
SELECT*FROM productsWHERE price>50000;
```

Meaning:

> Give me products costing more than ₹50,000.
> 

Later we will write much more complex queries.

---

# 9. SQL vs PostgreSQL

This distinction is very important.

### SQL

SQL is a **language**.

Example:

```
SELECT nameFROM products;
```

### PostgreSQL

PostgreSQL is the **database management system** that executes SQL.

Think:

```
You
 |
 | SQL
 v
PostgreSQL
 |
 v
Database
 |
 v
Result
```

### RDBMS

**RDBMS = Relational Database Management System**

Data is stored in **tables with rows and columns**, and tables can be related using keys.

Example: PostgreSQL

### NoSQL

**NoSQL = Non-relational database**

Data is generally stored as **documents, key-value pairs, graphs, or wide-column data**, rather than traditional relational tables.

Example: MongoDB

| RDBMS | NoSQL |
| --- | --- |
| Tables | Documents / key-value / other models |
| Fixed or well-defined schema | Flexible schema |
| Strong relationships | Often fewer joins |
| SQL is used | Query method depends on database |
| Strong ACID support | Consistency/transactions vary by system |
| Good for structured data | Good for flexible or very large-scale data |
| Example: PostgreSQL | Example: MongoDB |




Advantages and Disadvantages of DBMS
Advantages
Data Independence: Data independence is the concept that separates the way data is stored from the way it is accessed and used. It ensures that changes made to the structure of the database (schema) do not affect the applications using the data. There are two types of data independence: logical and physical.
Logical data independence allows modifications to the logical structure of the database without impacting the applications. For instance, if a new attribute needs to be added to a table or a relationship between tables is altered, applications accessing the data won't need to be rewritten. This flexibility is vital for adapting to changing business requirements without disrupting the existing software.
Physical data independence allows changes in the physical storage details of the database without affecting how data is accessed. For instance, the DBMS can decide to store data on different storage devices, reorganize data files for efficiency, or even change the file format used for storage. These changes can be made transparently to applications, ensuring that their operations remain unaffected.
Efficient Data Access: Efficient data access is a cornerstone of a well-designed DBMS, ensuring that data retrieval and manipulation are performed optimally.
Indexing: Indexes are data structures that speed up data retrieval by providing a quick way to locate specific rows in a table based on certain columns. For example, a database can use a B-tree index to efficiently find records matching a certain value without scanning the entire table. It uses indexing, query optimization, and caching techniques to speed up data access. This is especially important when dealing with large datasets, as it reduces the time it takes to retrieve information.
Query Optimization: Query optimization is the process of determining the most efficient way to execute a query. The DBMS's query optimizer analyzes different execution plans and selects the one that minimizes the time and resources needed to fetch the required data.
Caching: Caching involves storing frequently accessed data in memory. This reduces the need to fetch data from slower storage devices, such as hard drives, every time it's requested. Caching mechanisms enhance performance by providing faster data access for common queries.
Data Integrity: Data integrity refers to the accuracy, consistency, and reliability of the data stored in the database. A DBMS enforces data integrity constraints, such as uniqueness, referential integrity, and data validation rules. This ensures that the data stored in the database remains reliable and accurate over time.
Concurrent Access to Data: In a multi-user environment, multiple users or applications might need to access the same data simultaneously. A DBMS manages concurrent access by providing mechanisms like locking and transaction management. This ensures that data remains consistent even when accessed by multiple users concurrently.
Ensures Data Recovery: A DBMS includes features for data backup and recovery. Regular backups and transaction logs enable recovery in case of hardware failures, system crashes, or human errors. This helps prevent data loss and ensures business continuity.
Data Security: Data security is crucial to protect sensitive and confidential information. A DBMS provides security mechanisms to control who can access the data and what operations they can perform on it. This includes user authentication, authorization, and encryption of data stored in the database.
Control database redundancy → It can control data redundancy because it stores all the data in one single database file and that recorded data is placed in the database.
Database redundancy refers to the situation where the same data is stored multiple times in a database. Redundancy can lead to various issues, such as increased storage requirements, data inconsistency (due to multiple copies of the same data being updated differently), and difficulties in maintaining data accuracy.
Data sharing → In DBMS the authorized users of an organization can share the data among multiple users.
Easily maintenance → It can be easily maintained due to the centralized nature of the database system.
Reduce time → It reduces development time and maintenance need.
Backup → It provides backup and recovery subsystems which create automatic backup of data from hardware and software failure and restores the data if required.
Multiple user interface → It provides different types of user interface like graphical user interfaces, application program interfaces.
Disadvantages of DBMS
Cost of hardware and software → It requires a high speed of data processor and large memory size to run DBMS software.
Size → It occupies a large space of disks and large memory to run them efficiently.
Complexity → Database system creates additional complexity and requirements.
Higher impact of failure → Failure highly impacts the database because in most of the organization all the data stored in a single database and if the database is damaged due to electric failure or database corruption then the data may be lost forever.