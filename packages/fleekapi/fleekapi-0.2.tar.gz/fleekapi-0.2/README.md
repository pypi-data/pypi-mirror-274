# FleekAPI

FleekAPI is a lightweight [WSGI][] web application framework. It is designed
to make getting started quick and easy, with the ability to scale up to
complex applications. It began as a simple wrapper around [Jinja][], and will become one of the most popular Python web
application frameworks inshaaloh.

FleekAPI offers suggestions, but doesn't enforce any dependencies or
project layout. It is up to the developer to choose the tools and
libraries they want to use. There are many extensions provided by the
community that make adding new functionality easy.

[WSGI]: https://wsgi.readthedocs.io/
[Jinja]: https://jinja.palletsprojects.com/


## A Simple Example

```python
# save this as app.py
from fleekapi import FleekAPI

app = FleekAPI()

@app.route("/")
def hello(req, resp):
    resp.text = "Hello, World!"
```

```
$ gunicorn app:app
  [2024-05-21 01:34:43 +0500] [78175] [INFO] Starting gunicorn 22.0.0
  [2024-05-21 01:34:43 +0500] [78175] [INFO] Listening at: http://127.0.0.1:8000 (78175)
  [2024-05-21 01:34:43 +0500] [78175] [INFO] Using worker: sync
  [2024-05-21 01:34:43 +0500] [78176] [INFO] Booting worker with pid: 7817
    
  * Running on http://127.0.0.1:8000/ (Press CTRL+C to quit)
```


## Donate

The Avengers organization develops and supports FleekAPI. In order to grow the community of contributors and users, and
allow the maintainers to devote more time to the projects, [please
donate today][].

[please donate today]: https://t.me/toEpamMiddle
