import pygame
import sqlite3

# Define constants for GUI
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# initializing pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Product Management System")

# Connect to SQLite database
conn = sqlite3.connect('products.db')
c = conn.cursor()

# Check if the products table exists
c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='products' ''')
if c.fetchone()[0] == 0:
    c.execute('''CREATE TABLE products (
                 id INTEGER PRIMARY KEY,
                 name TEXT,
                 price REAL,
                 quantity INTEGER,
                 category TEXT
                 )''')
    conn.commit()


def add_product(name, price, quantity, category):
    # Connect to SQLite database
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    c.execute('''INSERT INTO products (name, price, quantity, category)
                 VALUES (?, ?, ?, ?)''', (name, price, quantity, category))
    conn.commit()

def get_products():
     # Connect to SQLite database
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM products")
    return c.fetchall()

def update_product(id, name, price, quantity, category):
     # Connect to SQLite database
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    
    c.execute('''UPDATE products
                 SET name=?, price=?, quantity=?, category=?
                 WHERE id=?''', (name, price, quantity, category, id))
    conn.commit()

def delete_product(id):
     # Connect to SQLite database
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    
    c.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Closing database connection
conn.close()
pygame.quit()
