import logging
from toybox.simpleapi import simple_view, run
from pyramid.security import Authenticated
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow


# please: pip install pyramid_jwt
"""
python ./jwt_server.py

# 403
$ http GET :8080/secure
# 200 OK
$ http GET :8080/login | tee /tmp/response.json
$ http GET :8080/secure X-Token:`cat /tmp/response.json | jq -r .token`
"""

logger = logging.getLogger(__name__)


@simple_view("/login")
def login_view(request):
    return {"token": request.create_jwt_token(1)}


@simple_view("/secure", permission="read")
def secure_view(request):
    return "OK"


class Root:
    __acl__ = [
        (Allow, Authenticated, ('read',)),
    ]

    def __init__(self, request):
        self.request = request


def includeme(config):
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.include('pyramid_jwt')
    config.set_root_factory(Root)
    config.set_jwt_authentication_policy('secret', http_header='X-Token')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run.include(includeme)
    run(port=8080)
