"""
Main application module for MySQL Connector demo.
Demonstrates MySQL database operations using mysql-connector-python with ClassicModels database.
"""

import mysql.connector
from db.mysql_client import mysql_client
from db.mysql_config import DB_CONFIG
from dal import (
    # Customer operations
    get_all_customers,
    get_customer_by_number,
    get_customers_by_country,
    
    # Order operations
    get_all_orders,
    get_order_by_number,
    get_order_details,
    get_orders_by_customer
)

def connect_and_query():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM customers LIMIT 3")
    records = cursor.fetchall()

    for record in records:
        print(record)


def main():
    """Main application entry point."""
    print("Starting ClassicModels MySQL Connector application...")
    print("="*60)
    
    # Connect to database
    connection = mysql_client.get_connection()
    
    if not connection or not connection.is_connected():
        print("Could not connect to database. Exiting.")
        return
    
    try:
        # Example 1: Get customers from a specific country
        print("\n1. CUSTOMERS IN USA:")
        print("-"*60)
        usa_customers = get_customers_by_country(connection, "USA")

        for customer in usa_customers[:5]:  # Show first 5
            print(f"Customer: {customer[1]}, City: {customer[5]}, Phone: {customer[4]}")
        
        # # Example 2: Get a specific customer and their orders
        # print("\n2. CUSTOMER DETAILS AND ORDERS:")
        # print("-"*60)
        # customer = get_customer_by_number(connection, 103)
        # if customer:
        #     print(f"Customer: {customer[1]}")
        #     print(f"Contact: {customer[3]} {customer[2]}")
        #     print(f"Location: {customer[7]}, {customer[11]}")
            
        #     # Get customer's orders
        #     orders = get_orders_by_customer(connection, 103)
        #     print(f"\nOrders: {len(orders)} total")
        #     for order in orders[:3]:  # Show first 3
        #         print(f"  - Order #{order[0]}, Date: {order[1]}, Status: {order[4]}")
        
        # # Example 3: Get all orders
        # print("\n3. RECENT ORDERS:")
        # print("-"*60)
        # recent_orders = get_all_orders(connection, limit=5)
        # for order in recent_orders:
        #     print(f"Order #{order[0]}, Date: {order[1]}, Customer: {order[5]}, Status: {order[4]}")
        
        # # Example 4: Get order details
        # print("\n4. ORDER DETAILS (Order #10100):")
        # print("-"*60)
        # order = get_order_by_number(connection, 10100)
        # if order:
        #     print(f"Order Date: {order[1]}, Status: {order[4]}")
            
        #     details = get_order_details(connection, 10100)
        #     print(f"Line Items: {len(details)}")
        #     for detail in details:
        #         print(f"  - {detail[2]} (Qty: {detail[3]}, Price: ${detail[4]})")
        
        print("\n" + "="*60)
        print("Application completed successfully")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Always close the connection
        if connection.is_connected():
            connection.close()
            print("Database connection closed")


if __name__ == "__main__":
    # main()
    connect_and_query()