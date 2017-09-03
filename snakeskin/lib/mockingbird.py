from contextlib import contextmanager
from functools import partial, wraps
import httpretty
import os

from flask import current_app


class MockResponse:
    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body

    def __call__(self, *args):
        return (self.status, self.headers, self.body)


_mock_registry = {}


def fixture(fixture_file):
    path = current_app.root_path + '/../fixtures/{}'.format(fixture_file)
    try:
        file = open(path)
    except FileNotFoundError:
        return MockResponse(404, {}, '{"message": "The requested resource was not found."}')
    with file:
        fixture = file.read()
        return MockResponse(200, {}, fixture)


def mockable(func):
   # if not _environment_supports_mocks():
   #     return func

    _mock_registry[func.__name__] = []

    @wraps(func)
    def mockable_wrapper(*args, **kw):
        if _environment_supports_mocks() and _mock_registry.get(func.__name__):
            mock_response = _mock_registry[func.__name__][-1](*args, **kw)
            kw['mock'] = partial(_activate_mock, mock_response=mock_response)
        else:
            kw['mock'] = _noop_mock
        return func(*args, **kw)
    return mockable_wrapper


def mocking(request_func):
    def register_mock_for_request_func(func):
        if _environment_supports_mocks():
            _register_mock(request_func, func)
        return func
    return register_mock_for_request_func


@contextmanager
def register(request_function, status, headers, body):
    def generate_mock_response(*args):
        return MockResponse(status, headers, body)
    _register_mock(request_function, generate_mock_response)
    yield
    _unregister_mock(request_function)


@contextmanager
def _activate_mock(url, mock_response):
    if mock_response and _environment_supports_mocks():
        httpretty.enable()
        # TODO handle methods other than GET
        httpretty.register_uri(httpretty.GET, url, body=mock_response)
        yield
        httpretty.disable()
    else:
        yield


def _environment_supports_mocks():
    env = os.environ.get('SNAKESKIN_ENV')
    return (env == 'test' or env == 'demo')


@contextmanager
def _noop_mock(url):
    yield None


def _register_mock(request_function, fixture_function):
    _mock_registry[request_function.__name__].append(fixture_function)


def _unregister_mock(request_function):
    _mock_registry[request_function.__name__].pop()
