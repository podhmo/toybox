with pyramid


```python
def support_datetime_response(config):
    from pyramid.renderers import JSON
    from datetime import datetime

    # override: json renderer
    json_renderer = JSON()

    def datetime_adapter(obj, request):
        return obj.isoformat()
    json_renderer.add_adapter(datetime, datetime_adapter)
    config.add_renderer('json', json_renderer)


if __name__ == "__main__":
    run.include(support_datetime_response)
    run(port=8080)
```
