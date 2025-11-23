"""
Database connection module.
Handles MySQL database connections with reconnection logic.
"""

import time
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from typing import Union, Optional
from db.mysql_config import DB_CONFIG

class MySqlClient:
    """
    Database connection manager with automatic retry logic and connection pooling.
    """
    
    def __init__(self, config: dict, attempts: int = 3, delay: int = 2):
        """
        Initialize database connection manager.
        
        Args:
            config: Database configuration dictionary
            attempts: Number of connection attempts (default: 3)
            delay: Base delay between retries in seconds (default: 2)
        """
        self.config = config
        self.attempts = attempts
        self.delay = delay
        self._connection: Optional[Union[MySQLConnectionAbstract, PooledMySQLConnection]] = None
    
    def connect(self) -> Union[MySQLConnectionAbstract, PooledMySQLConnection, None]:
        """
        Connect to MySQL database with automatic retry logic.
        
        Returns:
            MySQLConnection object or None if connection fails
        """
        attempt = 1
        
        while attempt < self.attempts + 1:
            try:
                self._connection = mysql.connector.connect(**self.config)
                print(f"Successfully connected to database: {self.config.get('database')}")
                return self._connection
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Access denied: Wrong username or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(f"Connection error: {err}")
                    
                if self.attempts == attempt:
                    print(f"Failed to connect after {self.attempts} attempts, exiting without a connection")
                    return None
                    
                print(f"Connection failed: {err}. Retrying ({attempt}/{self.attempts - 1})...")
                # Progressive reconnect delay (exponential backoff)
                time.sleep(self.delay ** attempt)
                attempt += 1
            except IOError as err:
                print(f"I/O error: {err}")
                if self.attempts == attempt:
                    return None
                time.sleep(self.delay ** attempt)
                attempt += 1
                
        return None
    
    def get_connection(self) -> Union[MySQLConnectionAbstract, PooledMySQLConnection, None]:
        """
        Get the current database connection or create a new one.
        
        Returns:
            MySQLConnection object or None if connection fails
        """
        if self._connection is None or not self.is_connected():
            return self.connect()
        return self._connection
    
    def is_connected(self) -> bool:
        """
        Check if the database connection is active.
        
        Returns:
            True if connected, False otherwise
        """
        if self._connection is None:
            return False
        try:
            return self._connection.is_connected()
        except:
            return False
    
    def close(self) -> None:
        """
        Close the database connection.
        """
        if self._connection and self.is_connected():
            self._connection.close()
            print("Database connection closed")
            self._connection = None
    
    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        test_conn = mysql.connector.connect(**self.config)
        
        if test_conn and test_conn.is_connected():
            print("Connection test successful")
            test_conn.close()
            return True
        else:
            print("Connection test failed")
            return False
    
    def __enter__(self):
        """
        Context manager entry point.
        """
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point.
        """
        self.close()
        return False

mysql_client = MySqlClient(DB_CONFIG)
