from magick import Magick

app = Magick()


@app.route('^/$')
def hello_world():
    return "<h1>Funciona!</h1>"


# @app.route('^/(?P<id>\d{1,})$')
# def somente_digito():
#     return "<h1>A URL desta página só contém digitos!</h1>"


# @app.route('^/new$')
# def somente_new():
#     return "<h1>A URL desta página só contém digitos!</h1>"


# @app.route('^/api$')
# def somente_new():
#     return {'message': 'Eu sou uma api'}



if __name__ == '__main__':
    app.run()
