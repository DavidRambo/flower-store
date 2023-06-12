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

During development, the TailwindCSS can be updated automatically by running a background process:

```
> tailwindcss -i src/flower_store/static/src/main.css -o src/flower_store/static/dist/main.css --watch
```

## TODO

- Shopping Cart
- Session management for shopping cart
- Wishlist for customers
  Allow customers to sign up for email notifications for the flowers they want.
