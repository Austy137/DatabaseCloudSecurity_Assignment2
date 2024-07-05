import sqlite3
import sys

def connect_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_table(conn):
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task TEXT NOT NULL);''')
        conn.commit()
    except Exception as e:
        print(e)

def add_task(conn, task):
    conn.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    conn.commit()

def list_tasks(conn):
    cursor = conn.execute('SELECT * FROM tasks ORDER BY id')
    print("To-Do List:")
    for row in cursor:
        print(f"{row[0]}: {row[1]}")

def delete_task(conn, task_id):
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    reset_task_ids(conn)

def reset_task_ids(conn):
    cursor = conn.execute('SELECT task FROM tasks ORDER BY id')
    tasks = cursor.fetchall()
    
    conn.execute('DROP TABLE IF EXISTS tasks')
    conn.execute('''CREATE TABLE tasks
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL);''')
    conn.commit()
    
    for task in tasks:
        conn.execute('INSERT INTO tasks (task) VALUES (?)', (task[0],))
    conn.commit()

def main():
    conn = connect_db()
    create_table(conn)
    
    if len(sys.argv) < 2:
        print("Usage: python todo_cli.py [add|list|delete] [task]")
        return
    
    command = sys.argv[1]
    
    if command == "add":
        task = " ".join(sys.argv[2:])
        add_task(conn, task)
    elif command == "list":
        list_tasks(conn)
    elif command == "delete":
        task_id = int(sys.argv[2])
        delete_task(conn, task_id)
    else:
        print("Unknown command")
    
    conn.close()

if __name__ == "__main__":
    main()
