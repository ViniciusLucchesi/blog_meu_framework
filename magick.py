import re
import cgi
import json
from wsgiref.simple_server import make_server
from jinja2 import Environment, FileSystemLoader



class Magick:
    """
    Magick is a new Python framework created just for fun!

    - OO abstração
    - Mapa de roteamento de URLs -> OK
    - Configuração de templates
    - Objeto calable WSGI
    - Método "run", que irá executar a aplicação
    """
    def __init__(self, template_folder: str="templates"):
        self.url_map = []
        self.env = Environment(loader=FileSystemLoader(template_folder))
    

    def route(self, rule, method="GET", template=None):
        def decorator(view):
            self.url_map.append(
                (rule, method, view, template)
            )
            return view
        return decorator


    def render_template(self, template_name, **context):
        template = self.env.get_template(template_name)
        return template.render(**context).encode('utf-8')
    

    def __call__(self, environ, start_resposne):
        body = b"Content not found"
        status = "404 Not Found"
        content_type = "text/html"

        # Processar o request
        path = environ["PATH_INFO"]
        request_method = environ["REQUEST_METHOD"]

        # Resolver a URL
        for rule, method, view, template in self.url_map:
            if (match := re.match(rule, path)):
                if method != request_method:
                    continue
                view_args = match.groupdict()
                view_result = view(**view_args)
                body = view_result.encode('utf-8')

        # Criar o response
        headers = [("Content-type", content_type)]
        start_resposne(status, headers)
        return [body]

    def run(self, host="0.0.0.0", port=8080):
        server = make_server(host, port, self)
        server.serve_forever()
    