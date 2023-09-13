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



@app.route('^/$', template="list.template.html")
def index():
    posts = get_posts_from_database()
    return { 'post_list': posts }


@app.route('^/(?P<id>\d{1,})$', template="post.template.html")
def post_detail(id: str):
    post = get_posts_from_database(post_id=id)[0]
    return {'post': post}
    


# @app.route('^/new$')
# def somente_new():
#     return "<h1>A URL desta página só contém digitos!</h1>"


# @app.route('^/api$')
# def somente_new():
#     return {'message': 'Eu sou uma api'}



if __name__ == '__main__':
    app.run()
