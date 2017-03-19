from datetime import datetime, timedelta
from pyramid.view import (
    view_config
)
from . import (
    schema
)
from toybox.swagger import (
    withswagger
)


@view_config(decorator=withswagger(schema.Input, schema.Output), renderer='vjson', request_method='GET', route_name='views')
def hello(context, request):
    """

    request.GET:

        * 'name'  -  `{"type": "string", "example": "Ada", "default": "Friend"}`
    """
    return {'message': 'Welcome, {}!'.format(request.GET["name"])}


@view_config(decorator=withswagger(schema.AddInput, schema.AddOutput), renderer='vjson', request_method='POST', route_name='views1')
def add(context, request):
    """


    request.json_body:

    ```
        {
          "type": "object",
          "properties": {
            "x": {
              "type": "integer"
            },
            "y": {
              "type": "integer"
            }
          },
          "required": [
            "x",
            "y"
          ]
        }
    ```
    """
    x = request.json["x"]
    y = request.json["y"]
    return {"result": x + y}


@view_config(decorator=withswagger(schema.DateaddInput, schema.DateaddOutput), renderer='vjson', request_method='POST', route_name='views2')
def dateadd(context, request):
    """


    request.json_body:

    ```
        {
          "type": "object",
          "properties": {
            "value": {
              "type": "string",
              "format": "date"
            },
            "addend": {
              "minimum": 1,
              "type": "integer"
            },
            "unit": {
              "type": "string",
              "default": "days",
              "enum": [
                "days",
                "minutes"
              ]
            }
          },
          "required": [
            "addend"
          ]
        }
    ```
    """
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
