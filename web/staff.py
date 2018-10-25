"""
Web authentication for staff members.

Author: Robin Wohlers-Reichel, Andrew Pope
Date: 25/10/2018
"""
from werkzeug.local import LocalProxy
from flask import g, current_app
import biz.manage_staff as ms
