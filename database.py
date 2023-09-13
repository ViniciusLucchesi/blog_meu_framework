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

posts = [
    {
        "title": "Python esta no top 5 das linguagens mais populares",
        "content": """
            O python é uma linguagem de programação de alto nível, interpretada, de script, imperativa, orientada a objetos, funcional, de tipagem dinâmica e forte. Foi lançada por Guido van Rossum em 1991. Atualmente possui um modelo de desenvolvimento comunitário, aberto e gerenciado pela organização sem fins lucrativos Python Software Foundation. Apesar de várias partes da linguagem possuírem padrões e especificações formais, a linguagem como um todo não é formalmente especificada. O padrão de facto é a implementação CPython.
        """, 
        "author": "Lucchesi"
    },
    {
        "title": "Rust, a linguagem de programacao que esta quebrando o mercado", 
        "content": """\
            Rust é uma linguagem de programação compilada, multi-paradigma, de tipagem estática, desenvolvida pela Mozilla Research, cujo projeto é liderado por Graydon Hoare. É projetada para ser "segura, concorrente e prática", suportando os estilos puramente funcional, imperativo procedimental, e concorrente. Foi concebida como uma linguagem de sistema, pois é compilada para código nativo, mas também foi projetada para ser uma linguagem de propósito geral. Rust é sintaticamente similar a C++, mas sua diferença mais marcante em relação a este é a garantia de segurança de memória da linguagem: ela impede que referências nulas ou apontadores livres ocorram no código. Rust também é uma linguagem multiparadigma que suporta programação funcional pura, procedimental imperativa, e até mesmo programação orientada a objetos (embora não seguindo o mesmo paradigma de linguagens como Java ou C++).
        """, 
        "author": "Lucchesi"
    },
]


count = cursor.execute("SELECT * FROM post;").fetchall()

if not count:
    cursor.executemany(
        """\
        INSERT INTO post (title, content, author) VALUES (:title, :content, :author);
        """,
        posts
    )
    conn.commit()
    print("Dados inseridos com sucesso!")

posts = cursor.execute("SELECT * FROM post;").fetchall()
assert len(posts) >= 2