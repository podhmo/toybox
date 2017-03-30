from pyramid.response import Response
from toybox.simple import simple_view


@simple_view("/")
def my_view(request):
    return Response("hello")
