import httpx
from database import conn
from magick import Magick

app = Magick()


def get_posts_from_database(post_id: int = None) -> list[dict[str, str]]:
    cursor = conn.cursor()
    fields = ('id', 'title', 'content', 'author')
    if post_id:
        results = cursor.execute('SELECT * FROM post WHERE id = ?;', post_id)
    else:
        results = cursor.execute('SELECT * FROM post;')
    return [dict(zip(fields, post)) for post in results]

def add_new_post(new_post: dict) -> None:
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO post (title, content, author) VALUES (:title, :content, :author)", new_post)
    conn.commit()


@app.route('^/$', template="list.template.html")
def index():
    posts = get_posts_from_database()
    return { 'post_list': posts }


@app.route('^/(?P<id>\d{1,})$', template="post.template.html")
def post_detail(id: str):
    post = get_posts_from_database(post_id=id)[0]
    return {'post': post}
    


@app.route('^/new$', template="form.template.html")
def new():
    return {}


@app.route('^/new$', method="POST", template="list.template.html")
def new_post(form):
    # Getting and Setting the new post to the Database
    post = {item.name: item.value for item in form.list}
    add_new_post(post)

    # Get all posts from de database
    posts = get_posts_from_database()
    return { 'post_list': posts }



if __name__ == '__main__':
    app.run()
