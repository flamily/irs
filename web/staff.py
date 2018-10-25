"""
Web authentication for staff members.

Author: Robin Wohlers-Reichel, Andrew Pope
Date: 25/10/2018
"""
from werkzeug.local import LocalProxy
from web.db import db
from flask import g, current_app
from flask import (
    redirect,
    url_for, Blueprint, render_template,
    request, session
)

import biz.manage_staff as ms

def authenticate():
    if not session['username']:
        # Redirect to login page
        return

    # Get password??
    password = 'dummy'
    if not ms.verify_password(db, session['username'], password):
        # Redirect to login page
        return

    # Return staff member?
    return


staff = LocalProxy(authenticate)
