# -*- coding:utf-8 -*-
import logging
from toybox.simpleapi import run
from pyramid_rpc.jsonrpc import jsonrpc_method

# please: pip install pyramid_rpc
# see also: http://docs.pylonsproject.org/projects/pyramid_rpc/en/latest/jsonrpc.html
"""
python ./jsonrpc_server.py
$ echo '{"id": "1", "params": {"name": "foo"}, "method": "say_hello", "jsonrpc": "2.0"}' | http POST :8080/api
{
    "id": "1",
    "jsonrpc": "2.0",
    "result": "hello, foo"
}
"""


@jsonrpc_method(endpoint='api')
def say_hello(request, name):
    return 'hello, {}'.format(name)


def includeme(config):
    config.include('pyramid_rpc.jsonrpc')
    config.add_jsonrpc_endpoint('api', '/api')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run.include(includeme)
    run(port=8080)
