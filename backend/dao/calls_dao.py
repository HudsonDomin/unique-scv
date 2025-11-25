from .database_setup import get_db_connection
from ..models.user_model import User

class CallsDAO:
    def insert_user(self, user: User):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user.name, user.email)
        )
        conn.commit()
        return cursor.lastrowid
    
    # ... outros métodos CRUD (get_user, update_user, delete_user)