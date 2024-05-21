from functools import wraps

from flask import current_app, redirect, request, session
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS, USE_SESSION_FOR_NEXT
from flask_login.utils import expand_login_view
from flask_login.utils import login_url as make_login_url
from flask_login.utils import make_next_param


def role_required(roles: list[str]):
    """
    This decorator works identically to login_required, accept that it
    additionally requires that a user have their role attribute
    set to 'role'. If the current user is authenticated,
    but does not have `role == ROLE`, the user is sent to the
    :attr:`LoginManager.no_role` callback.
    """

    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if request.method in EXEMPT_METHODS or current_app.config.get(
                "LOGIN_DISABLED"
            ):
                pass
            # The role privilege is checked below.
            # Here, role privilege is given to users whose attribute `role == role`,
            # but this can be customized to require any desired specification.
            elif current_user.role not in roles:
                return current_app.login_manager.no_role()
            return func(*args, **kwargs)

        return decorated_view

    return decorator


def no_role(self):
    # This method of LoginManager requires that you provide a `no_role_view` attribute to LoginManager.
    # `no_role_view` can be provided where you provide a `login_view` for unauthorized users.
    no_role_view = self.no_role_view
    config = current_app.config
    if config.get("USE_SESSION_FOR_NEXT", USE_SESSION_FOR_NEXT):
        no_role_url = expand_login_view(no_role_view)
        session["_id"] = self._session_identifier_generator()
        session["next"] = make_next_param(no_role_url, request.url)
        redirect_url = make_login_url(no_role_view)
    else:
        redirect_url = make_login_url(no_role_view, next_url=request.url)
    return redirect(redirect_url)
