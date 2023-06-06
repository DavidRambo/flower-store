# flower-store

Store for selling flowers built on Flask.

## Installation

flower-store uses [pip-tools](pypi.org/project/pip-tools) to manage dependencies and [Hatch](hatch.pypa.io) as its build system.
If you want to run the server, then run:

```
> pip-sync requirements.txt
```

If you want to develop, then run:

```
> pip-sync dev-requirements.txt
> pip install -e .
```

Either way, to setup the database:

```
> flask db upgrade
```

The `run.py` script exposes some dev functions from `dev_fns.py` in the shell:
```
> flask shell

>>> popf()  # populates the database with Flower table entries
>>> ca()  # creates a user with admin privileges
```

### TailwindCSS

To minify the css using pytailwindcss:

```
> tailwindcss -i src/flower_store/static/src/main.css -o src/flower_store/static/dist/main.css --minify
```

### OpenSearch

The site uses OpenSearch as an index for full-text search.

If on MacOS:
```
To start opensearch now and restart at login:
  brew services start opensearch
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/opensearch/bin/opensearch
```

Otherwise, on Linux:
```
...
```

OpenSearch provides a high-level Python client (opensearch-dsl-py)[https://opensearch.org/docs/latest/clients/python-high-level/]
for common interactions with an OpenSearch index.

## TODO

* Full-text search
* Shopping Cart
* Session management for shopping cart
* Wishlist for customers
    Allow customers to sign up for email notifications for the flowers they want.
