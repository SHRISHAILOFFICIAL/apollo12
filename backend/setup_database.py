"""
Database Setup Script for DCET Platform

This script helps create the MySQL database for the DCET platform.
Run this script to create the database if it doesn't exist.

Usage:
    python setup_database.py

Note: Make sure MySQL is running and you have the correct credentials.
"""

import mysql.connector
from mysql.connector import Error

def create_database():
    """Create the dcet_platform database if it doesn't exist."""
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'  # Update with your MySQL root password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS dcet_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✓ Database 'dcet_platform' created successfully or already exists")
            
            # Show existing databases
            cursor.execute("SHOW DATABASES")
            print("\nAvailable databases:")
            for (database,) in cursor:
                if database == 'dcet_platform':
                    print(f"  → {database} (DCET Platform Database)")
                else:
                    print(f"    {database}")
            
            cursor.close()
            connection.close()
            print("\n✓ Database setup completed successfully!")
            print("\nNext steps:")
            print("1. Update PASSWORD in backend/config/settings.py DATABASES configuration")
            print("2. Run: python manage.py makemigrations")
            print("3. Run: python manage.py migrate")
            
    except Error as e:
        print(f"✗ Error connecting to MySQL: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL is running")
        print("2. Update the password in this script if needed")
        print("3. Check your MySQL credentials")

if __name__ == "__main__":
    create_database()
