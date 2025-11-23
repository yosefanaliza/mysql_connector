# MySQL Connector Python Application

A Python application demonstrating best practices for MySQL database connectivity using `mysql-connector-python`.

## Project Structure

```
sql-connector/
├── config.py              # Database configuration (credentials)
├── main.py               # Main application entry point
├── db/
│   ├── __init__.py       # Package initialization
│   ├── connection.py     # Database connection logic with retry
│   └── queries.py        # SQL queries and operations
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Features

- ✅ Secure configuration management (separate config file)
- ✅ Automatic connection retry with exponential backoff
- ✅ Comprehensive error handling
- ✅ Logging to console and file
- ✅ Parameterized queries (SQL injection prevention)
- ✅ Context managers for cursor operations
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ InnoDB tables with proper indexes
- ✅ Transaction management

## Installation

1. **Clone or navigate to the project directory**

2. **Create a virtual environment** (recommended):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

## Configuration

1. **Update `config.py`** with your MySQL database credentials:
   ```python
   DB_CONFIG = {
       'user': 'your_username',
       'password': 'your_password',
       'host': '127.0.0.1',
       'port': 3306,
       'database': 'your_database',
       'raise_on_warnings': True,
       'use_pure': False
   }
   ```

2. **Alternatively, use environment variables** (optional):
   - Copy `.env.example` to `.env`
   - Update values in `.env`
   - Modify `config.py` to read from environment variables

## Usage

Run the main application:

```powershell
python main.py
```

The application will:
1. Connect to MySQL database with automatic retry
2. Create a sample `users` table
3. Insert sample user data
4. Query and display users
5. Update a user's email
6. Delete a user
7. Display remaining users

## Key Conventions Used

Based on [MySQL Connector/Python Documentation](https://dev.mysql.com/doc/connector-python/en/):

- **Configuration separation**: Credentials in `config.py` (never hardcoded)
- **Error handling**: Comprehensive try-except blocks with specific error codes
- **Parameterized queries**: All queries use `%s` placeholders to prevent SQL injection
- **Connection management**: Automatic retry with exponential backoff
- **Logging**: Both console and file logging for debugging
- **Context managers**: Cursors used within `with` statements
- **InnoDB engine**: Tables created with InnoDB for ACID compliance
- **Indexes**: Proper indexing on frequently queried columns
- **C Extension**: Uses C extension by default for better performance

## Database Operations

### Create Table
```python
create_sample_table(connection)
```

### Insert Data
```python
user_id = insert_data(connection, "username", "email@example.com")
```

### Query Data
```python
users = query_data(connection, limit=10)
user = query_user_by_id(connection, user_id)
```

### Update Data
```python
update_user_email(connection, user_id, "newemail@example.com")
```

### Delete Data
```python
delete_user(connection, user_id)
```

## Logging

Logs are written to:
- **Console**: Real-time output
- **File**: `mysql-connector.log` (persistent logging)

## Security Best Practices

- ✅ Never commit credentials to version control
- ✅ Use parameterized queries (prevents SQL injection)
- ✅ Validate and sanitize user input
- ✅ Use `.gitignore` to exclude sensitive files
- ✅ Store credentials in environment variables or secure vaults

## Requirements

- Python 3.7+
- MySQL Server 5.7+ or 8.0+
- mysql-connector-python 8.0+

## License

This is a demonstration project for educational purposes.
