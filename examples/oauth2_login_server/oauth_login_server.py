# -*- coding:utf-8 -*-
import logging
import uuid
import argparse
import urllib.parse as p
from toybox.simpleapi import simple_view, run
from zope.interface import Interface
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from rauth import OAuth2Service

# please: pip install rauth
"""
python oauth_login_server --client-id=<> --client-secret=<>
open http://localhost:5000/login
"""


class IGithubAuthenticator(Interface):
    # todo: description
    pass


class GithubAuthenticator(object):
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.store = {}  # don't use this in production

    @reify
    def service(self):
        return OAuth2Service(
            client_id=self.client_id,
            client_secret=self.client_secret,
            name='github',
            authorize_url='https://github.com/login/oauth/authorize',
            access_token_url='https://github.com/login/oauth/access_token',
            base_url='https://api.github.com/'
        )

    def get_state_token(self, name):
        if name not in self.store:
            self.store[name] = p.quote_plus("{}:{}".format(name, uuid.uuid4().hex))
        return self.store[name]


@simple_view("/callback")
def callback(request):
    github = request.registry.getUtility(IGithubAuthenticator)
    assert request.GET["state"] == github.get_state_token("<username>")  # using session
    token = github.service.get_access_token(data={'code': request.GET["code"]})
    print("access token: ", token)
    raise HTTPFound(location=request.route_url("api-issues", _query={"token": token}))


@simple_view("/api/issues", route_name="api-issues")
def get_issues(request):
    if "token" not in request.GET:
        raise HTTPNotFound("token not found")
    github = request.registry.getUtility(IGithubAuthenticator)
    auth_session = github.service.get_session(request.GET["token"])
    return auth_session.get('/repos/podhmo/toybox/issues').json()


@simple_view("/login")
def login(request):
    github = request.registry.getUtility(IGithubAuthenticator)
    # https://developer.github.com/v3/oauth/#scopes
    authorize_url = github.service.get_authorize_url(scope='repo', state=github.get_state_token("<username>"))
    raise HTTPFound(location=authorize_url)


def includeme(config):
    settings = config.registry.settings
    ob = GithubAuthenticator(settings["client_id"], settings["client_secret"])
    config.registry.registerUtility(ob, IGithubAuthenticator)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--client-secret", required=True)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    run.include(includeme)
    run(port=5000, settings={"client_id": args.client_id, "client_secret": args.client_secret})
