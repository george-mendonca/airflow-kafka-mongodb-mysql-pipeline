import mysql.connector
from pymongo import MongoClient

# MySQL Configuration
mysql_config = {
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'host': 'localhost',
    'database': 'your_database_name'
}

# MongoDB Configuration
mongodb_config = {
    'host': 'localhost',
    'port': 27017,
    'database': 'your_mongodb_name'
}

# Function to initialize MySQL tables
def init_mysql_tables():
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price DECIMAL(10, 2), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sales (id INT AUTO_INCREMENT PRIMARY KEY, product_id INT, quantity INT, sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS logs (id INT AUTO_INCREMENT PRIMARY KEY, message TEXT, log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        conn.commit()
    except mysql.connector.Error as e:
        print(f'Error initializing MySQL tables: {e}')
    finally:
        if conn:
            cursor.close()
            conn.close()

# Function to initialize MongoDB collections
def init_mongodb_collections():
    client = MongoClient(mongodb_config['host'], mongodb_config['port'])
    db = client[mongodb_config['database']]
    
    # Create collections
    db.create_collection('raw_data')
    db.create_collection('processed_data')
    db.create_collection('logs')

# Main function
if __name__ == '__main__':
    init_mysql_tables()
    init_mongodb_collections()
    print('Database initialization complete.')