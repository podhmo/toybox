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
    return {}


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
    return {}


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
    return {}