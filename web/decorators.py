from werkzeug.local import LocalProxy
from functools import wraps
from flask import (
    session, request, render_template, redirect, url_for
)
from web.db import db
import biz.manage_staff as ms


def templated(template=None):  # pragma: no cover
    def decorator(incoming_func):
        @wraps(incoming_func)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = incoming_func(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


def login_required():  # add optional parameter to control groups
    def decorator(incoming_func):
        @wraps(incoming_func)
        def decorated_function(*args, **kwargs):
            if not session.get('username', None):
                return redirect(url_for('login.index', next=request.url))
            return incoming_func(*args, **kwargs)
        return decorated_function
    return decorator


def get_user():
    """Retrieve the user record (staff) from the db for the session."""
    username = session.get('username', None)
    if not username:
        # This block is necessary in the event that the programmer has
        # forgotten to use the `login_required` decorator in an endpoint
        # accessing the user LocalProxy
        raise RuntimeError(
            "attempt to access a user without authentication"
        )  # pragma: no cover

    staff_mb = ms.get_staff_member(db, username)
    if not staff_mb:
        raise LookupError(
            "no staff record exists for username: {}".format(username)
        )

    return staff_mb


user = LocalProxy(get_user)
