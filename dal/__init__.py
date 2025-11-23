"""Data Access Layer package initialization for ClassicModels database."""

from .customer_dal import (
    get_all_customers,
    get_customer_by_number,
    get_customers_by_country,
    get_customers_by_sales_rep,
    insert_customer,
    update_customer,
    delete_customer
)

from .order_dal import (
    get_all_orders,
    get_order_by_number,
    get_orders_by_customer,
    get_orders_by_status,
    insert_order,
    update_order_status,
    get_order_details
)

__all__ = [
    # Customer operations
    'get_all_customers',
    'get_customer_by_number',
    'get_customers_by_country',
    'get_customers_by_sales_rep',
    'insert_customer',
    'update_customer',
    'delete_customer',
    
    # Order operations
    'get_all_orders',
    'get_order_by_number',
    'get_orders_by_customer',
    'get_orders_by_status',
    'insert_order',
    'update_order_status',
    'get_order_details'
]
