# MySQL Connector - ClassicModels Database

A Python application demonstrating MySQL database connectivity using `mysql-connector-python` with the ClassicModels sample database. Features a clean Data Access Layer (DAL) architecture with class-based connection management.

## Project Structure

```
sql-connector/
├── config.py                  # Database configuration with environment variables
├── main.py                    # Main application with examples
├── db/
│   ├── __init__.py           # Database package exports
│   ├── mysql_client.py       # MySqlClient class with retry logic
│   └── mysql_config.py       # Database configuration
├── dal/                       # Data Access Layer
│   ├── __init__.py           # DAL package exports
│   ├── customer_dal.py       # Customer operations
│   └── order_dal.py          # Order & OrderDetails operations
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Features

- ✅ **Class-based connection management** with `MySqlClient`
- ✅ **Automatic retry logic** with exponential backoff
- ✅ **Environment variable configuration** using python-dotenv
- ✅ **Data Access Layer (DAL)** for clean separation of concerns
- ✅ **Parameterized queries** for SQL injection prevention
- ✅ **Context manager support** for automatic resource cleanup
- ✅ **Comprehensive error handling** with specific MySQL error codes
- ✅ **ClassicModels database** operations (Customers & Orders)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yosefanaliza/mysql_connector.git
   cd mysql_connector
   ```

2. **Create a virtual environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

## Configuration

1. **Create `.env` file** from the example:
   ```powershell
   copy .env.example .env
   ```

2. **Update `.env`** with your MySQL credentials:
   ```env
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_NAME=classicmodels
   ```

## Usage

### Run the Application

```powershell
python main.py
```

The application demonstrates:
1. Querying customers by country
2. Getting customer details and their orders
3. Listing recent orders
4. Retrieving order details with line items

### Using the MySqlClient Class

```python
from db.mysql_client import MySqlClient
from db.mysql_config import DB_CONFIG

# Initialize client
client = MySqlClient(DB_CONFIG, attempts=3, delay=2)

# Get connection
connection = client.get_connection()

# Use connection for database operations
if client.is_connected():
    # Your database operations here
    pass

# Close connection
client.close()
```

### Using Context Manager

```python
from db.mysql_client import MySqlClient
from db.mysql_config import DB_CONFIG

# Automatic connection and cleanup
with MySqlClient(DB_CONFIG) as client:
    conn = client.get_connection()
    # Do database operations
# Connection automatically closed
```

### Using the Singleton Instance

```python
from db.mysql_client import mysql_client

# Get connection from singleton
connection = mysql_client.get_connection()

# Use connection
if connection.is_connected():
    # Your operations
    pass
```

## Data Access Layer (DAL)

### Customer Operations

```python
from dal import (
    get_all_customers,
    get_customer_by_number,
    get_customers_by_country,
    get_customers_by_sales_rep,
    insert_customer,
    update_customer,
    delete_customer
)

# Get customers from USA
usa_customers = get_customers_by_country(connection, "USA")

# Get specific customer
customer = get_customer_by_number(connection, 103)

# Update customer
update_customer(connection, 103, creditLimit=75000.00)
```

### Order Operations

```python
from dal import (
    get_all_orders,
    get_order_by_number,
    get_orders_by_customer,
    get_orders_by_status,
    get_order_details,
    insert_order,
    update_order_status
)

# Get all orders for a customer
orders = get_orders_by_customer(connection, 103)

# Get order details
order = get_order_by_number(connection, 10100)
details = get_order_details(connection, 10100)

# Update order status
update_order_status(connection, 10100, "Shipped")
```

## Architecture

### MySqlClient Class

The `MySqlClient` class provides:
- **Automatic retry logic**: Exponentially backs off on connection failures
- **Connection state tracking**: `is_connected()` method
- **Context manager support**: Use with `with` statement
- **Singleton pattern**: Pre-initialized `mysql_client` instance available

### Data Access Layer Pattern

The DAL provides:
- **Separation of concerns**: Database logic isolated from business logic
- **Reusable functions**: Common operations encapsulated
- **Type safety**: Proper type hints for all parameters
- **Error handling**: Consistent error messages and rollback logic
- **Parameterized queries**: Protection against SQL injection

## ClassicModels Database

This application uses the [ClassicModels](https://www.mysqltutorial.org/mysql-sample-database.aspx) sample database, which models a business that sells scale models of classic cars.

### Tables Used:
- **customers**: Customer information and sales representatives
- **orders**: Order header information (dates, status)
- **orderdetails**: Order line items (products, quantities, prices)

## Security Best Practices

- ✅ **Environment variables**: Credentials stored in `.env` (gitignored)
- ✅ **Parameterized queries**: All SQL uses `%s` placeholders
- ✅ **No hardcoded secrets**: Configuration separated from code
- ✅ **Connection validation**: Proper connection state checking
- ✅ **Error handling**: No sensitive data in error messages

## Dependencies

```
mysql-connector-python>=8.0.0
python-dotenv>=1.0.0
```

## Requirements

- Python 3.7+
- MySQL Server 5.7+ or 8.0+
- ClassicModels database installed

## License

This is a demonstration project for educational purposes.

## Contributing

Feel free to submit issues or pull requests to improve this project.

## Contact

Repository: [https://github.com/yosefanaliza/mysql_connector](https://github.com/yosefanaliza/mysql_connector)
