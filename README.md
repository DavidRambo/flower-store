# flower-store

Store for selling flowers built on Flask.
Since I don't currently intend to sell flowers, I have not integrated payment processing.

See it live here: [flowers.davidrambo.org](https://flowers.davidrambo.org)

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

During development, the TailwindCSS can be updated automatically by running a background process:

```
> tailwindcss -i src/flower_store/static/src/main.css -o src/flower_store/static/dist/main.css --watch
```

### Elasticsearch

Elasticsearch is implemented on the `elasticsearch` branch.
The `main` branch uses case-insensitive SQL queries.
It works well enough, but it cannot handle fuzzy search in the way elasticsearch does.

When using elasticsearch during development, I run it on my workstation.
If you do this, remember to stop the process when you're done.

## TODO

- Wishlist for customers
  Allow customers to sign up for email notifications for the flowers they want.
