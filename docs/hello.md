hello world

```python
from toybox.simpleapi import simple_view, run


@simple_view("/hello/{name}", route_name="hello")
def hello(request):
    return {"message": "hello {}".format(request.matchdict["name"])}

if __name__ == "__main__":
    run(port=8080)
```

another command (this is experimental, maybe changing in the near future)

```
if __name__ == "__main__":
    run(port=8080)
    # run.pshell()
    # run.proutes()
    # run.ptweens()
    # run.handle_request()
```
