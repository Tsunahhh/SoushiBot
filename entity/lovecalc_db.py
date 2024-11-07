import sqlite3
import os

class LoveCalcDB:
    def __init__(self) -> None:

        self.path = "data/members.db"

        dir_path = os.path.dirname(self.path)
        if not os.path.exists(dir_path):
            os.makedirs(os.path.dirname(self.path))

        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS love_results (
                user1_id TEXT NOT NULL,
                user2_id TEXT NOT NULL,
                love_percent INTEGER NOT NULL,
                PRIMARY KEY (user1_id, user2_id)
            )
        ''')

        self.conn.commit()

    def get_love_percent(self, user1_id, user2_id):
        # Récupérer le pourcentage de compatibilité entre deux utilisateurs
        self.cursor.execute('''
            SELECT love_percent FROM love_results
            WHERE (user1_id = ? AND user2_id = ?)
               OR (user1_id = ? AND user2_id = ?)
        ''', (user1_id, user2_id, user2_id, user1_id))
        
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def save_love_percent(self, user1_id, user2_id, love_percent):
        # Enregistrer le pourcentage de compatibilité entre deux utilisateurs
        self.cursor.execute('''
            INSERT OR REPLACE INTO love_results (user1_id, user2_id, love_percent)
            VALUES (?, ?, ?)
        ''', (user1_id, user2_id, love_percent))
        self.conn.commit()

    def close(self):
        # Fermer la connexion à la base de données
        self.conn.close()     