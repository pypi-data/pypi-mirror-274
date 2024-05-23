# app.py
import inspect
import os

import requests
import wsgiadapter
from jinja2 import Environment, FileSystemLoader
from parse import parse
from webob import Request
from werkzeug.serving import run_simple
from whitenoise import WhiteNoise
from icecream import ic

from .middleware import Middleware
from .response import Response


def html_response(resp, content):
    resp.html = content
    return resp


def default_response(resp):
    resp.status_code = 404
    resp.html = "Page not found"
    return resp


def method_not_allowed(resp):
    resp.status_code = 405
    resp.html = "Method not allowed"
    return resp


class FleekAPI:
    def __init__(self):
        self.routes = dict()
        self.template_env = Environment(loader=FileSystemLoader(os.path.abspath("templates")))
        self.exception_handler = None
        self.whitenoise = WhiteNoise(self.wsgi_app, root="static", prefix="/static")
        self.middleware = Middleware(self)

    def __call__(self, environ, start_response):
        path_info = environ["PATH_INFO"]
        if path_info.startswith("/static"):
            return self.whitenoise(environ, start_response)
        return self.middleware(environ, start_response)

    def wsgi_app(self, environ, start_response):
        req = Request(environ)
        resp = self.handle_request(req)
        return resp(environ, start_response)

    def handle_request(self, req):
        handler_data, kwargs = self.find_handler(req)
        resp = Response()
        if handler_data is not None:
            handler = handler_data["handler"]
            allowed_methods = handler_data["allowed_methods"]
            if inspect.isclass(handler):
                handler = getattr(handler(), req.method.lower(), None)
                if handler is None:
                    return method_not_allowed(resp)
            else:
                if req.method.lower() not in allowed_methods:
                    return method_not_allowed(resp)
            try:
                content = handler(**kwargs)
                return html_response(resp, content=content)
            except Exception as e:
                if self.exception_handler is not None:
                    self.exception_handler(e, req, resp)
                else:
                    raise e
        else:
            return default_response(resp)
        return resp

    def find_handler(self, req):
        for path, handler_data in self.routes.items():
            parsed_result = parse(path, req.path)
            if parsed_result is not None:
                return handler_data, parsed_result.named
        return None, None

    def add_route(self, path, handler, allowed_methods=["get"]):
        assert path not in self.routes, "Duplicate route. Please change the URL."
        self.routes[path] = {"handler": handler, "allowed_methods": allowed_methods}

    def route(self, path, allowed_methods=None):
        if allowed_methods is None:
            allowed_methods = ["get"]
        def decorator(func):
            self.add_route(path, func, allowed_methods)
            return func
        return decorator

    def test_session(self):
        session = requests.Session()
        session.mount('http://testserver/', wsgiadapter.WSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        if context is None:
            context = dict()
        template = self.template_env.get_template(template_name).render(**context)
        return template

    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)

    def include_router(self, router):
        self.routes.update(router.routes)

    def run(self, debug=False):
        run_simple("localhost", 8000, self, use_reloader=debug, use_debugger=debug, use_evalex=debug)


class Router(FleekAPI):
    def __init__(self):
        super().__init__()
        self.routes = dict()
