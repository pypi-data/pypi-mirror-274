import json
import traceback
from typing import List, Tuple

from flask_projects.core.vars.application import application
from flask_projects.default.middle.NameFactory import name_extend
from flask_projects.default.middle.convention import OutContextBeforeMiddle, OutContextBackMiddle, \
    InContextBeforeMiddle, InContextBackMiddle, MiddleException
from flask_projects.interface.container import ContainerAbs
from flask_projects.interface.logic import LogicAbs


class WsgiAppMethodReplacementCls:

    def __init__(
            self,
            old_wsgi_app,
            middles: Tuple[
                List[OutContextBeforeMiddle],
                List[InContextBeforeMiddle],
                List[InContextBackMiddle],
                List[OutContextBackMiddle]
            ]
    ):

        self.old_wsgi_app = old_wsgi_app
        self.middles = middles

    def before_in_context(self):
        for middle in self.middles[1]:
            middle.option_before_in_context()

    def back_in_context(self, response):
        for middle in self.middles[2]:
            response = middle.option_back_in_context(response)

        return response

    def __call__(self, environ, start_response):

        # 请求前拦截器
        try:
            for middle_bf in self.middles[0]:      # 请求处理前后两处for循环的遍历内容其实是一样的，只是为了便于区分所以使用了不同的变量名
                middle_bf.option_before_out_context(environ, start_response)
        except MiddleException as e:
            response = {
                "code": e.code,
                "message": e.description
            }
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps(response).encode('utf-8')]
        except Exception as e:
            print(traceback.format_exc())
            response = {
                "code": 500,
                "message": "option_before_out_context处发生未知错误"
            }
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps(response).encode('utf-8')]

        # 请求处理
        response = self.old_wsgi_app(environ, start_response)

        # 请求后拦截器
        try:
            for middle_bk in self.middles[3]:
                response = middle_bk.option_back_out_context(response)
        except MiddleException as e:
            response = {
                "code": e.code,
                "message": e.description
            }
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps(response).encode('utf-8')]
        except Exception:
            print(traceback.format_exc())
            response = {
                "code": 500,
                "message": "option_back_out_context处发生未知错误"
            }
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps(response).encode('utf-8')]

        return response


class Plan0MiddleLogic(LogicAbs):
    name = name_extend

    def execute(self, container: ContainerAbs):
        middles = container.query()

        app = application.getter_app()
        new_wsgi_app = WsgiAppMethodReplacementCls(app.wsgi_app, middles)

        app.wsgi_app = new_wsgi_app
        app.before_request(new_wsgi_app.before_in_context)
        app.after_request(new_wsgi_app.back_in_context)
