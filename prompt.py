natural_language_to_structure = '''
# Role
- You are a very helpful database assistant.
- Please translate the provided natural language query into a json using the database meta-information below.
- Output a valid JSON only.

# Database Meta-information
{database_meta_information}

# Output Requirement for JSON
- "Relevance": 
    - If the user's query is not related to the above meta-information, set it as "Irrelevant Query". In this case, set all the following keys to empty strings.
    - Otherwise, set to "Relevant Query".
- "Tables_Involved": list all tables involved (comma-separated).
- "Structure": describe each SQL clause of user input using SQL-like structured natural language (one clause per line, no actual SQL code).

# Output Example
{
    "Relevance": "Relevant Query",
    "Tables_Involved": "Users, Orders",
    "Structure": "Get the Full_Name and Email from Users\nJoin Users and Orders on User_Id"
}

# Additional Guidance
- Use the exact column names and table names as in the meta-information.
- Consider synonyms and natural language variations (e.g., 'customer' and 'user').
- If the query is ambiguous, make reasonable assumptions.

# User Input
{user_input}
'''

structure_to_sql = '''
# Role
- You are a very helpful SQL assistant.
- Please translate the provided structured natural language query into a real SQL code using the database meta-information below.
- Output SQL code only.

# Database Meta-information
{database_meta_information}

# Output Requirement for SQL
- Use only table and column names from the meta-information.

# Structured Input
{user_input}
'''

sql_code_check = '''
# Role
- You are a very helpful evaluator tasked with reviewing SQL code for correctness and identifying fatal errors.  
- Output a valid JSON only.

# Taxonomy of Fatal Errors
- Code is incomplete (e.g., truncated, unfinished statements).
- SQL syntax (grammar) errors.
- Table or column names do not match the database meta-information.

# Database Meta-information
{database_meta_information}


# Output Requirement for JSON
- If a fatal error is detected
[
  {"inconsistency": "<inconsistency1>", "explanation": "<explanation1>"},
  ...
]

- If no fatal error is detected
[
  {"inconsistency": "Negligible"}
]

# SQL Code
{user_input}
'''

database_meta_information = '''
## 1. Products Table

| Column Name     | Data Type         | Description                       | Key Info         |
|-----------------|------------------|------------------------------------|------------------|
| Product_Id      | INT (AUTO_INCREMENT) | Unique product ID                | PRIMARY KEY      |
| Name            | VARCHAR(255)     | Product name                       |                  |
| Category        | VARCHAR(100)     | Product category                   |                  |
| Provider        | VARCHAR(100)     | Supplier/Provider name             |                  |
| Price           | DECIMAL(10,2)    | Unit price                         |                  |
| Quantity        | INT              | Available stock quantity           |                  |
| Description     | TEXT             | Detailed product description       |                  |
| Created_At      | DATETIME         | When the product was added         |                  |
| Updated_At      | DATETIME         | Last update timestamp              |                  |

---

## 2. Users Table

| Column Name     | Data Type         | Description                       | Key Info         |
|-----------------|------------------|------------------------------------|------------------|
| User_Id         | INT (AUTO_INCREMENT) | Unique user/customer ID         | PRIMARY KEY      |
| Full_Name       | VARCHAR(150)     | Full name of the user              |                  |
| Email           | VARCHAR(255)     | User email address                 | UNIQUE           |
| Phone           | VARCHAR(20)      | Phone number (optional)            |                  |
| Address         | VARCHAR(255)     | Mailing address                    |                  |
| Registered_At   | DATETIME         | Registration date                  |                  |
| Status          | ENUM('active', 'inactive') | Current status              |                  |

---

## 3. Orders Table

| Column Name     | Data Type         | Description                       | Key Info         |
|-----------------|------------------|------------------------------------|------------------|
| Order_Id        | INT (AUTO_INCREMENT) | Unique order ID                  | PRIMARY KEY      |
| User_Id         | INT              | Customer who made the order        | FOREIGN KEY (Users.User_Id) |
| Order_Date      | DATETIME         | Date/time of order                 |                  |
| Total_Amount    | DECIMAL(10,2)    | Total order value                  |                  |
| Status          | ENUM('pending', 'shipped', 'delivered', 'cancelled') | Order status |                  |
| Shipping_Address| VARCHAR(255)     | Shipping address for the order     |                  |

---

## 4. OrderDetails Table

| Column Name     | Data Type         | Description                       | Key Info         |
|-----------------|------------------|------------------------------------|------------------|
| OrderDetail_Id  | INT (AUTO_INCREMENT) | Unique order detail ID          | PRIMARY KEY      |
| Order_Id        | INT              | Reference to Orders table          | FOREIGN KEY (Orders.Order_Id)|
| Product_Id      | INT              | Reference to Products table        | FOREIGN KEY (Products.Product_Id)|
| Quantity        | INT              | Quantity ordered                   |                  |
| Unit_Price      | DECIMAL(10,2)    | Price per unit at time of order    |                  |

---

## 5. Reviews Table

| Column Name     | Data Type         | Description                       | Key Info         |
|-----------------|------------------|------------------------------------|------------------|
| Review_Id       | INT (AUTO_INCREMENT) | Unique review ID                 | PRIMARY KEY      |
| Product_Id      | INT              | Reviewed product                   | FOREIGN KEY (Products.Product_Id)|
| User_Id         | INT              | Reviewer (customer)                | FOREIGN KEY (Users.User_Id)|
| Rating          | INT              | Rating (1–5 stars)                 |                  |
| Comment         | TEXT             | Review comment                     |                  |
| Review_Date     | DATETIME         | Submission date                    |                  |

---
'''