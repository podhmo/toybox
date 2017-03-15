import logging
from toybox.simpleapi import simple_view, run
from pyramid.httpexceptions import HTTPBadRequest


"""
$ python ./paginaion_server.py
$ http :4444/value
$ http :4444/value offset==10
$ http :4444/value offset==10 limit==20
$ http :4444/value offset==100 limit==10
$ http :4444/value offset==99 limit==10
$ http :4444/value offset==101 limit==10
"""

logger = logging.getLogger(__name__)


L = list(range(1, 101))
assert len(L) == 100


@simple_view("/value")
def value(request):
    logger.info("requested")
    try:
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 10))
    except ValueError as e:
        raise HTTPBadRequest(str(e))
    value = L[offset:][:limit]
    return {"value": value, "offset": offset, "limit": limit, "count": len(value)}


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
    run(port=4444)
