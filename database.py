import aiosqlite
from datetime import datetime

DEFAULT_DB = 'visits.db'

async def init_db(db_path=DEFAULT_DB):
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                user_agent TEXT,
                visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def add_visit(ip: str, user_agent: str = None, db_path=DEFAULT_DB):
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            'INSERT INTO visits (ip, user_agent) VALUES (?, ?)',
            (ip, user_agent)
        )
        await db.commit()

async def get_stats(period: str = 'all', db_path=DEFAULT_DB):
    async with aiosqlite.connect(db_path) as db:
        query = 'SELECT COUNT(*) as total, COUNT(DISTINCT ip) as unique_visits FROM visits'
        
        if period == 'day':
            query += " WHERE date(visit_time) = date('now')"
        elif period == 'month':
            query += " WHERE strftime('%Y-%m', visit_time) = strftime('%Y-%m', 'now')"
        elif period == 'year':
            query += " WHERE strftime('%Y', visit_time) = strftime('%Y', 'now')"
        
        cursor = await db.execute(query)
        result = await cursor.fetchone()
        return {
            'total': result[0],
            'unique': result[1]
        }
