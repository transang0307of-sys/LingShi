"""Quản lý database operations"""
import sqlite3
import json
from datetime import datetime
from config import DB_NAME

def init_db():
    """Khởi tạo database"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_states
                 (user_id INTEGER PRIMARY KEY,
                  personality TEXT DEFAULT 'tsundere',
                  mood TEXT DEFAULT 'bình thường',
                  sect TEXT DEFAULT 'thanh_van',
                  user_role TEXT DEFAULT 'su_de',
                  conversation_history TEXT DEFAULT '[]',
                  last_updated TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_user_state(user_id):
    """Lấy state của user"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT personality, mood, sect, user_role, conversation_history FROM user_states WHERE user_id = ?', 
              (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return {
            'personality': result[0],
            'mood': result[1],
            'sect': result[2],
            'user_role': result[3],
            'history': json.loads(result[4])
        }
    else:
        create_user(user_id)
        return {
            'personality': 'tsundere',
            'mood': 'bình thường',
            'sect': 'thanh_van',
            'user_role': 'su_de',
            'history': []
        }

def create_user(user_id):
    """Tạo user mới"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO user_states 
                 (user_id, personality, mood, sect, user_role, conversation_history, last_updated)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (user_id, 'tsundere', 'bình thường', 'thanh_van', 'su_de', '[]', datetime.now()))
    conn.commit()
    conn.close()

def update_user_state(user_id, personality=None, mood=None, sect=None, user_role=None, history=None):
    """Cập nhật state của user"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    if personality:
        c.execute('UPDATE user_states SET personality = ?, last_updated = ? WHERE user_id = ?',
                  (personality, datetime.now(), user_id))
    if mood:
        c.execute('UPDATE user_states SET mood = ?, last_updated = ? WHERE user_id = ?',
                  (mood, datetime.now(), user_id))
    if sect:
        c.execute('UPDATE user_states SET sect = ?, last_updated = ? WHERE user_id = ?',
                  (sect, datetime.now(), user_id))
    if user_role:
        c.execute('UPDATE user_states SET user_role = ?, last_updated = ? WHERE user_id = ?',
                  (user_role, datetime.now(), user_id))
    if history is not None:
        limited_history = history[-10:] if len(history) > 10 else history
        c.execute('UPDATE user_states SET conversation_history = ?, last_updated = ? WHERE user_id = ?',
                  (json.dumps(limited_history), datetime.now(), user_id))
    
    conn.commit()
    conn.close()
