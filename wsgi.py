import cgi
import json
from jinja2 import Environment, FileSystemLoader
from database import conn
from surreal import SurrealDB


env = Environment(loader=FileSystemLoader('.'))


def get_posts_from_database(post_id: int = None) -> list[dict[str, str]]:
    cursor = conn.cursor()
    fields = ('id', 'title', 'content', 'author')
    if post_id:
        results = cursor.execute('SELECT * FROM post WHERE id = ?;', post_id)
    else:
        results = cursor.execute('SELECT * FROM post;')
    return [dict(zip(fields, post)) for post in results]

# async def get_posts_from_surreldb(post_id: int = None):
#     if post_id:
#         results = SurrealDB.query(f'SELECT * FROM post WHERE id = {post_id};')
#     else:
#         results = SurrealDB.query('SELECT * FROM posts;')
#     return results


def render_template(template_name: str, **context) -> str:
    template = env.get_template(template_name)
    return template.render(**context).encode('utf-8')


def add_new_post(new_post: dict) -> None:
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO post (title, content, author) VALUES (:title, :content, :author)", new_post)
    conn.commit()



async def application(environ, start_response):
    # Processar o request
    path = environ["PATH_INFO"]
    content_type = 'text/html'
    method = environ["REQUEST_METHOD"]
    body = b"Content not found"
    status = "404 Not Found"

    # Roteamento das URLs
    if path == "/" and method == "GET":
        posts = get_posts_from_database()
        body = render_template(
            "list.template.html",
            post_list=posts
        )
    elif path == "/api" and method == "GET":
        posts = get_posts_from_database()
        content_type = "application/json"
        body = json.dumps(posts).encode()
        status = "200 OK"

    # elif path == "/api/surreal" and method == "GET":
    #     posts = await get_posts_from_surreldb()
    #     content_type = "application/json"
    #     body = json.dumps(posts).encode()
    #     status = "200 OK"

    elif path.split("/")[-1].isdigit() and method == "GET":
        status = "200 OK"
        post_id = path.split("/")[-1]
        body = render_template(
            "post.template.html",
            post=get_posts_from_database(post_id)[0]
        )
    elif path == "/new" and method == "GET":
        status = "200 OK"
        body = render_template("form.template.html")
    elif path == "/new" and method == "POST":
        form = cgi.FieldStorage(
            fp = environ['wsgi.input'],
            environ = environ,
            keep_blank_values=1
        )
        post = {item.name: item.value for item in form.list}
        add_new_post(post)

        status = "201 Created"
        body = b"Postagem inserida com sucesso!"
        


    # Construir a responsta
    headers = [("Content-Type", content_type)]
    start_response(status, headers)
    return [body]
