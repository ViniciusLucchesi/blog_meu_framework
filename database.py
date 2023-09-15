from sqlite3 import connect

conn = connect('blog.db')
cursor = conn.cursor()

conn.execute(
    """\
    CREATE TABLE IF NOT EXISTS post (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR UNIQUE NOT NULL,
        content VARCHAR NOT NULL,
        author VARCHAR NOT NULL
    )
    """
)
