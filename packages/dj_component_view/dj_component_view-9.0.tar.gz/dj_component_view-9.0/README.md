# dj_component_view

This project lets you create reusable Django views from [jinjax](https://jinjax.scaletti.dev/) templates.

## Usage

### Greeting.jinja

```jinja
<h1>hello, {{ name }}</h1>
```

### views.py

```python
from djecorator import Route
from dj_component_view import component

route = Route()

@route("/components/greet")
@component("Greeting")
def greet(request):
    return {
        "name": request.GET.get("name", "World"),
    }
```


### index.html with [htmx](https://htmx.org)

```html
<form hx-get="{{ url('greet') }}" hx-trigger="submit">
  <input type="text" name="name" placeholder="Enter your name" />
  <button type="submit">Greet</button>
</form>
```

There is also a lower-level API which the `component` decorator uses under the hood.
The `ComponentView` class inherits from django's own `View` class.


```python
from dj_component_view import ComponentView
from djecorator import Route

route = Route()

@route("/greet", name="greet")
class GreetView(ComponentView):
    component = "Greeting"

    def render(self, request):
        return {
            "name": request.GET.get("name", "World"),
        }
```

### Specifying the Allowed HTTP Methods

You can set the `methods` class variable in your ComponentView subclass to specify the allowed HTTP methods for the view. The default value is `["GET"]`.

- If `methods` is set to `["GET"]`, only GET requests will be allowed.
- If `methods` is set to `["POST"]`, only POST requests will be allowed.
- If `methods` is set to `["GET", "POST"]`, both GET and POST requests will be allowed.

```python
@component("CustomComponent", methods=["post"])
def custom_component(request):
    ...

# or

class CustomView(ComponentView):
    component = "CustomComponent"
    methods = ["post"]

    ...

```

If the incoming request's method does not match any of the specified methods, a 405 Method Not Allowed response will be returned.

### Overriding the get and post Methods

If you need more control over the handling of GET and POST requests, you can override the get and post methods in your ComponentView subclass.

```python
@route("/custom")
class CustomView(ComponentView):
    component = "CustomComponent"
    methods = ["get"]

    def get(self, request, *args, **kwargs):
        # Custom implementation of the GET method
        ...
```
