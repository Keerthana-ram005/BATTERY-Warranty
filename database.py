import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta


DB_NAME = "warranty.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


# -------------------- CREATE TABLES --------------------

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Users (Admin Login)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Customers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile_number TEXT UNIQUE NOT NULL
        )
    """)

    # Warranty Details
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warranties(
            warranty_id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            warranty_period INTEGER NOT NULL,
            warranty_type TEXT NOT NULL
        )
    """)

    # Purchases
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases(
            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            brand TEXT NOT NULL,
            product_type TEXT NOT NULL,
            serial_number TEXT UNIQUE NOT NULL,
            quantity INTEGER NOT NULL,
            purchase_date TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            photo_path TEXT,
            warranty_id INTEGER,

            FOREIGN KEY(customer_id)
            REFERENCES customers(customer_id),

            FOREIGN KEY(warranty_id)
            REFERENCES warranties(warranty_id)
        )
    """)

    # Claims
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims(
            claim_id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER NOT NULL,
            claim_date TEXT NOT NULL,
            claim_reason TEXT,
            claim_status TEXT DEFAULT 'Completed',

            FOREIGN KEY(purchase_id)
            REFERENCES purchases(purchase_id)
        )
    """)

    conn.commit()
    conn.close()


# -------------------- USER FUNCTIONS --------------------

def add_user(user_name, password, role):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users(user_name, password, role)
        VALUES(?,?,?)
    """, (user_name, password, role))

    conn.commit()
    conn.close()


def login_user(user_name, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE user_name=? AND password=?
    """, (user_name, password))

    user = cursor.fetchone()

    conn.close()

    return user


# -------------------- CUSTOMER FUNCTIONS --------------------

def add_customer(name, mobile):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO customers(name, mobile_number)
        VALUES(?,?)
    """, (name, mobile))

    conn.commit()
    conn.close()


def get_customer_by_mobile(mobile):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM customers
        WHERE mobile_number=?
    """, (mobile,))

    customer = cursor.fetchone()

    conn.close()

    return customer


# -------------------- WARRANTY FUNCTIONS --------------------

def add_warranty(brand, period, warranty_type):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO warranties(
        brand,
        warranty_period,
        warranty_type)
        VALUES(?,?,?)
    """, (brand, period, warranty_type))

    warranty_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return warranty_id


# -------------------- DATE CALCULATION --------------------

def calculate_expiry_date(purchase_date, warranty_period):

    date_obj = datetime.strptime(
        purchase_date,
        "%Y-%m-%d"
    )

    expiry = date_obj + relativedelta(
        months=warranty_period
    )

    return expiry.strftime("%Y-%m-%d")


# -------------------- PURCHASE FUNCTIONS --------------------

def add_purchase(
        customer_id,
        brand,
        product_type,
        serial_number,
        quantity,
        purchase_date,
        photo_path,
        warranty_id,
        warranty_period
):

    expiry_date = calculate_expiry_date(
        purchase_date,
        warranty_period
    )

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO purchases(
        customer_id,
        brand,
        product_type,
        serial_number,
        quantity,
        purchase_date,
        expiry_date,
        photo_path,
        warranty_id
        )
        VALUES(?,?,?,?,?,?,?,?,?)
    """, (
        customer_id,
        brand,
        product_type,
        serial_number,
        quantity,
        purchase_date,
        expiry_date,
        photo_path,
        warranty_id
    ))

    conn.commit()
    conn.close()

# -------------------- CLAIMS --------------------

def add_claim(purchase_id, claim_reason):

    conn = connect_db()
    cursor = conn.cursor()

    claim_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO claims(
            purchase_id,
            claim_date,
            claim_reason
        )
        VALUES(?,?,?)
    """, (
        purchase_id,
        claim_date,
        claim_reason
    ))

    conn.commit()
    conn.close()

def get_claim_history(purchase_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            claim_date,
            claim_reason,
            claim_status
        FROM claims

        WHERE purchase_id = ?

        ORDER BY claim_date DESC
    """, (purchase_id,))

    data = cursor.fetchall()

    conn.close()

    return data

# -------------------- CUSTOMER PURCHASE COUNT --------------------

def get_customer_purchase_count(mobile):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM purchases

        JOIN customers
        ON purchases.customer_id = customers.customer_id

        WHERE customers.mobile_number = ?
    """, (mobile,))

    count = cursor.fetchone()[0]

    conn.close()

    return count

# -------------------- SEARCH CUSTOMER PURCHASES --------------------

def get_customer_data(mobile):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            purchases.purchase_id,
            customers.name,
            customers.mobile_number,
            purchases.brand,
            purchases.product_type,
            purchases.serial_number,
            purchases.quantity,
            purchases.purchase_date,
            purchases.expiry_date,
            purchases.photo_path,
            warranties.warranty_period,
            warranties.warranty_type

        FROM purchases

        JOIN customers
        ON purchases.customer_id = customers.customer_id

        JOIN warranties
        ON purchases.warranty_id = warranties.warranty_id

        WHERE customers.mobile_number = ?
    """, (mobile,))

    data = cursor.fetchall()

    conn.close()

    return data