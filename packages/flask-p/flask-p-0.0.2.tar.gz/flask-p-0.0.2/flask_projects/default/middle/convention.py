from abc import ABCMeta, abstractmethod
from typing import Optional

from werkzeug.exceptions import HTTPException


class MiddleException(HTTPException):

    code = 500
    description = 'Middle Error'

    def __init__(self, msg: str):
        self.description = msg


class BasicMiddle(metaclass=ABCMeta):
    """
        本类型实现子类时，不可使用含参初始化方法
    """
    sort: Optional[int] = None

    def __new__(cls):

        assert cls.sort is not None, "attribute named 'sort' of BasicMiddle type cannot be None"

        return super().__new__(cls)


class OutContextBeforeMiddle(BasicMiddle):

    @abstractmethod
    def option_before_out_context(self, environ, start_response):

        ...


class OutContextBackMiddle(BasicMiddle):

    @abstractmethod
    def option_back_out_context(self, response):

        return response


class InContextBeforeMiddle(BasicMiddle):

    @abstractmethod
    def option_before_in_context(self):
        ...


class InContextBackMiddle(BasicMiddle):

    @abstractmethod
    def option_back_in_context(self, response):

        return response
