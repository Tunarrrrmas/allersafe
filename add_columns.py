import sqlite3
from datetime import datetime

# Path to your database
db_path = 'recipe.db'

try:
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add columns without complex defaults first
    try:
        cursor.execute('ALTER TABLE recipe ADD COLUMN status TEXT DEFAULT "approved"')
        print("Added status column")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Status column already exists")
        else:
            print(f"Error adding status column: {e}")
    
    try:
        cursor.execute('ALTER TABLE recipe ADD COLUMN author_id INTEGER')
        print("Added author_id column")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Author_id column already exists")
        else:
            print(f"Error adding author_id column: {e}")
    
    # Add submitted_at without default, then update existing rows
    try:
        cursor.execute('ALTER TABLE recipe ADD COLUMN submitted_at DATETIME')
        print("Added submitted_at column")
        
        # Update existing rows with current timestamp
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('UPDATE recipe SET submitted_at = ? WHERE submitted_at IS NULL', (current_time,))
        print(f"Updated existing rows with timestamp: {current_time}")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Submitted_at column already exists")
        else:
            print(f"Error adding submitted_at column: {e}")
    
    # Commit all changes
    conn.commit()
    print("Database updated successfully!")
    
    # Verify the changes
    cursor.execute("PRAGMA table_info(recipe)")
    columns = cursor.fetchall()
    print("\nCurrent table structure:")
    for col in columns:
        print(f"- {col[1]} ({col[2]})")
    
    # Show sample data
    cursor.execute("SELECT id, name, status, author_id, submitted_at FROM recipe LIMIT 3")
    rows = cursor.fetchall()
    print("\nSample data:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Status: {row[2]}, Author: {row[3]}, Submitted: {row[4]}")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
finally:
    if conn:
        conn.close()