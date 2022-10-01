from flask import g, url_for, redirect
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, "user"):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))
    return wrapper