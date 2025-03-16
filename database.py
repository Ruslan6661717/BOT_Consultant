
import aiosqlite

DB_NAME = "knowledge.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT UNIQUE,
                answer TEXT
            )
        """)
        await db.commit()


async def get_answer(question: str):
    question = question.lower().strip()
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT answer FROM knowledge WHERE question = ?", (question,))
        result = await cursor.fetchone()
        return result[0] if result else None


async def add_answer(question: str, answer: str):
    question = question.lower().strip()
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO knowledge (question, answer) VALUES (?, ?)", (question, answer))
        await db.commit()


async def delete_answer(question: str):
    question = question.lower().strip()
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM knowledge WHERE question = ?", (question,))
        await db.commit()


async def list_questions():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT question FROM knowledge")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]