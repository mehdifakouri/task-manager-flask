import os
import psycopg
from dotenv import load_dotenv


load_dotenv()
#تلاش برای اتصال

def get_connection():
    """یک اتصال جدید به دیتابیس برمیگرداند"""
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="task_manager",
        user="postgres",
        password= os.getenv("DB_PASSWORD")
    )

def create_task(title, description=""):
    """یک تسک جدید در دیتابیس میساز و ایدی آن را برمیگرداند"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (title, description)
                VALUES (%s, %s)
                returning id
                """,
                (title, description)
            )
            task_id = cur.fetchone()[0]
        conn.commit()
    return task_id

def get_all_tasks():
    """همه تسک ها را برمیگرداند"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, description, completed, created_at
                FROM tasks
                ORDER BY created_at DESC
                """
            )
            return cur.fetchall()

def get_task(task_id):
    """یک تسک خاص را با ایدی برمیگرداند"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, description, completed, created_at
                FROM tasks
                WHERE id = %s
                """,
                (task_id,)
            )
            return cur.fetchone()

def mark_completed(task_id):
    """تسک را به عنوان انجام شده علامت میزند"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET completed = TRUE
                WHERE id = %s
                """,
                (task_id,)
            )
        conn.commit()

def delete_task(task_id):
    """تسک را حذف میکند"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM tasks
                WHERE id = %s
                """,
                (task_id,)
            )
        conn.commit()

if __name__ == '__main__':
    print("db.py loaded successfully.")

