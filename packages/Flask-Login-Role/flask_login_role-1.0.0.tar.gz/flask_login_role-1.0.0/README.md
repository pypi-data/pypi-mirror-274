# Flask-Login-Role

A super light-weight alternative to Flask-User or Flask-Security that adds role requirements for views to Flask-Login.

## Features

### `role_required`

This decorator requires that a user be authenticated and have their role attribute set to one of the roles specified. If the current user is authenticated but does not have their role in the specified roles, the user is sent to the `LoginManager.no_role` callback.

### `no_role`

This method of `LoginManager` requires that you provide a `no_role_view` attribute to `LoginManager`. `no_role_view` can be provided where you provide a `login_view` for unauthorized users.

## Installation

```
pip install Flask-Login-Role@git+https://github.com/glyzinieh/flask-login-role
```

## Usage

See [examples/app.py](examples/app.py) for an example of proper set up.

- `User` model will need a `role` attribute with the required permissions.
- `from flask_login_role import no_role`, and add a `no_role` method to `LoginManager`
- Give `LoginManager` a `no_role_view` attribute that is a string that indicates which view function to redirect authorized but unprivileged users to.
- `from flask_login_role import role_required` wherever routes are defined, and decorate privilleged routes.

## Thanks

Thanks to [@schwartz721](https://github.com/schwartz721/role_required) for creating the project from which we forked.
