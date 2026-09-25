import sqlite3
import pandas as pd

def build_database():
    conn = sqlite3.connect("zepto_catalog.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price_gbp REAL,
        price_inr REAL,
        rating INTEGER,
        in_stock INTEGER,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (category_id)
    );
    """)
    
    df = pd.read_csv("cleaned_books.csv")
    
    for cat in df['category_name'].unique():
        cursor.execute("INSERT OR IGNORE INTO categories (category_name) VALUES (?)", (cat,))
    conn.commit()
    
    cat_map = pd.read_sql("SELECT category_id, category_name FROM categories", conn)
    cat_dict = dict(zip(cat_map['category_name'], cat_map['category_id']))
    
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO books (title, price_gbp, price_inr, rating, in_stock, category_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (row['title'], row['price_gbp'], row['price_inr'], row['rating'], row['in_stock'], cat_dict[row['category_name']]))
    conn.commit()
    
    q_join = """
    SELECT b.title, b.price_gbp, b.rating, c.category_name 
    FROM books b JOIN categories c ON b.category_id = c.category_id 
    WHERE b.rating >= 4
    """
    sql_res = pd.read_sql(q_join, conn)
    print(sql_res.head())
    
    conn.close()

if __name__ == "__main__":
    build_database()import sqlite3
import pandas as pd

def build_database():
    conn = sqlite3.connect("zepto_catalog.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price_gbp REAL,
        price_inr REAL,
        rating INTEGER,
        in_stock INTEGER,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (category_id)
    );
    """)
    
    df = pd.read_csv("cleaned_books.csv")
    
    for cat in df['category_name'].unique():
        cursor.execute("INSERT OR IGNORE INTO categories (category_name) VALUES (?)", (cat,))
    conn.commit()
    
    cat_map = pd.read_sql("SELECT category_id, category_name FROM categories", conn)
    cat_dict = dict(zip(cat_map['category_name'], cat_map['category_id']))
    
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO books (title, price_gbp, price_inr, rating, in_stock, category_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (row['title'], row['price_gbp'], row['price_inr'], row['rating'], row['in_stock'], cat_dict[row['category_name']]))
    conn.commit()
    
    q_join = """
    SELECT b.title, b.price_gbp, b.rating, c.category_name 
    FROM books b JOIN categories c ON b.category_id = c.category_id 
    WHERE b.rating >= 4
    """
    sql_res = pd.read_sql(q_join, conn)
    print(sql_res.head())
    
    conn.close()

if __name__ == "__main__":
    build_database()
