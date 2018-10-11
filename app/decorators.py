from functools import wraps
from flask import session, request, render_template, redirect, url_for


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


def login_required(allow=['management']):
    def decorator(incoming_func):
        @wraps(incoming_func)
        def decorated_function(*args, **kwargs):
            # if g.user is None:
            if not session.get('username', None):
                return redirect(url_for('login.index', next=request.url))
            return incoming_func(*args, **kwargs)
        return decorated_function
    return decorator
