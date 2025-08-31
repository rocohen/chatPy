import sqlite3
import os
from datetime import datetime

def init_database():
    """Inicializamos la base de datos SQLite con la tabla de mensajes"""
    try:
        conn = sqlite3.connect('chat_msgs.db')
        cursor = conn.cursor()
        
        # Crear tabla según los campos requeridos en la consigna
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
                ip_cliente TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error inicializando la base de datos: {e}")
        return False

def save_message(contenido, ip_cliente):
    """Guardamos un mensaje en la base de datos"""
    try:
        conn = sqlite3.connect('chat_msgs.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (contenido, ip_cliente, fecha_envio)
            VALUES (?, ?, ?)
        ''', (contenido, ip_cliente, datetime.now()))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error guardando mensaje en BD: {e}")
        return False

def check_database_access():
    """Verificamos si la base de datos es accesible"""
    try:
        conn = sqlite3.connect('chat_msgs.db')
        conn.close()
        return True
    except sqlite3.Error:
        return False