from datetime import datetime, timedelta
from toybox.simpleapi import simple_view, run
from toybox.swagger import withswagger
import schema  # ./schema.py


@simple_view("/", decorator=withswagger(input=schema.Input, output=schema.Output))
def hello(request):
    return {'message': 'Welcome, {}!'.format(request.GET["name"])}


@simple_view("/add", request_method="POST", decorator=withswagger(input=schema.AddInput, output=schema.AddOutput))
def add(request):
    x = request.json["x"]
    y = request.json["y"]
    return {"result": x + y}


@simple_view("/dateadd", request_method="POST", decorator=withswagger(input=schema.DateaddInput, output=schema.DateaddOutput))
def dateadd(request):
    value = request.json["value"]
    addend = request.json["addend"]
    unit = request.json["unit"]
    value = value or datetime.utcnow()
    if unit == 'minutes':
        delta = timedelta(minutes=addend)
    else:
        delta = timedelta(days=addend)
    result = value + delta
    return {'result': result}


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    run.include("toybox.swagger")
    run(port=5001)
