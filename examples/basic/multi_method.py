from toybox.simpleapi import simple_view, run


@simple_view("/", request_method="GET")
def get(request):
    return "GET: hello"


@simple_view("/", request_method="POST")
def post(request):
    return "POST: hello"


@simple_view("/", request_method="DELETE")
def delete(request):
    return "DELETE: hello"


@simple_view("/", request_method="PUT")
def put(request):
    return "PUT: hello"


@simple_view("/", request_method="PATCH")
def patch(request):
    return "PATCH: hello"


if __name__ == "__main__":
    run()
