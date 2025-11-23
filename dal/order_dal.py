"""
Order Data Access Layer.
Handles all database operations related to orders and orderdetails tables.
"""

from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from typing import Optional, List, Any, Union
from datetime import date


def get_all_orders(connection: Union[MySQLConnectionAbstract, PooledMySQLConnection],
                  limit: int = 100) -> List[Any]:
    """
    Get all orders from the database.
    
    Args:
        connection: Active MySQL connection
        limit: Maximum number of rows to return
        
    Returns:
        List of order tuples
    """
    query = '''
    SELECT orderNumber, orderDate, requiredDate, shippedDate, 
           status, customerNumber
    FROM orders
    ORDER BY orderDate DESC
    LIMIT %s
    '''
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            print(f"Retrieved {len(rows)} orders")
            return rows
    except Exception as err:
        print(f"Failed to query orders: {err}")
        return []


def get_order_by_number(connection: Union[MySQLConnectionAbstract, PooledMySQLConnection],
                       order_number: int) -> Optional[Any]:
    """
    Get an order by order number.
    
    Args:
        connection: Active MySQL connection
        order_number: Order number
        
    Returns:
        Order tuple or None if not found
    """
    query = '''
    SELECT orderNumber, orderDate, requiredDate, shippedDate, 
           status, comments, customerNumber
    FROM orders
    WHERE orderNumber = %s
    '''
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (order_number,))
            row = cursor.fetchone()
            return row
    except Exception as err:
        print(f"Failed to query order: {err}")
        return None


def get_orders_by_customer(connection: Union[MySQLConnectionAbstract, PooledMySQLConnection],
                          customer_number: int) -> List[Any]:
    """
    Get all orders for a specific customer.
    
    Args:
        connection: Active MySQL connection
        customer_number: Customer number
        
    Returns:
        List of order tuples
    """
    query = '''
    SELECT orderNumber, orderDate, requiredDate, shippedDate, status
    FROM orders
    WHERE customerNumber = %s
    ORDER BY orderDate DESC
    '''
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (customer_number,))
            rows = cursor.fetchall()
            print(f"Found {len(rows)} orders for customer {customer_number}")
            return rows
    except Exception as err:
        print(f"Failed to query orders by customer: {err}")
        return []


def get_orders_by_status(connection: Union[MySQLConnectionAbstract, PooledMySQLConnection],
                        status: str) -> List[Any]:
    """
    Get orders by status.
    
    Args:
        connection: Active MySQL connection
        status: Order status (Shipped, Resolved, Cancelled, On Hold, Disputed, In Process)
        
    Returns:
        List of order tuples
    """
    query = '''
    SELECT orderNumber, orderDate, requiredDate, shippedDate, 
           customerNumber, status
    FROM orders
    WHERE status = %s
    ORDER BY orderDate DESC
    '''
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (status,))
            rows = cursor.fetchall()
            print(f"Found {len(rows)} orders with status '{status}'")
            return rows
    except Exception as err:
        print(f"Failed to query orders by status: {err}")
        return []


def insert_order(connection: Union[MySQLConnectionAbstract, PooledMySQLConnection],
                order_number: int, order_date: date, required_date: date,
                customer_number: int, status: str = "In Process") -> bool:
    """
    Insert a new order.
    
    Args:
        connection: Active MySQL connection
        order_number: Order number
        order_date: Order date
        required_date: Required date
        customer_number: Customer number
        status: Order status (default: In Process)
        
    Returns:
        True if successful, False otherwise
    """
    query = '''
    INSERT INTO orders (orderNumber, orderDate, requiredDate, customerNumber, status)
    VALUES (%s, %s, %s, %s, %s)
    '''
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (order_number, order_date, required_date,
                                 customer_number, status))
            connection.commit()
            print(f"Order {order_number} inserted successfully")
            return True
    except Exception as err:
        print(f"Failed to insert order: {err}")
        connection.rollback()
        return False


def update_order_status(connection: Union[MySQLConnectionAbstract, PooledMySQLConnection],
                       order_number: int, status: str, 
                       shipped_date: Optional[date] = None) -> bool:
    """
    Update order status and optionally shipped date.
    
    Args:
        connection: Active MySQL connection
        order_number: Order number
        status: New status
        shipped_date: Shipped date (optional)
        
    Returns:
        True if successful, False otherwise
    """
    if shipped_date:
        query = "UPDATE orders SET status = %s, shippedDate = %s WHERE orderNumber = %s"
        values = (status, shipped_date, order_number)
    else:
        query = "UPDATE orders SET status = %s WHERE orderNumber = %s"
        values = (status, order_number)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            connection.commit()
            if cursor.rowcount > 0:
                print(f"Order {order_number} status updated to '{status}'")
                return True
            else:
                print(f"No order found with number {order_number}")
                return False
    except Exception as err:
        print(f"Failed to update order status: {err}")
        connection.rollback()
        return False


def get_order_details(connection: Union[MySQLConnectionAbstract, PooledMySQLConnection],
                     order_number: int) -> List[Any]:
    """
    Get order details (line items) for a specific order.
    
    Args:
        connection: Active MySQL connection
        order_number: Order number
        
    Returns:
        List of order detail tuples
    """
    query = '''
    SELECT od.orderNumber, od.productCode, p.productName, 
           od.quantityOrdered, od.priceEach, od.orderLineNumber
    FROM orderdetails od
    JOIN products p ON od.productCode = p.productCode
    WHERE od.orderNumber = %s
    ORDER BY od.orderLineNumber
    '''
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (order_number,))
            rows = cursor.fetchall()
            print(f"Found {len(rows)} line items for order {order_number}")
            return rows
    except Exception as err:
        print(f"Failed to query order details: {err}")
        return []
