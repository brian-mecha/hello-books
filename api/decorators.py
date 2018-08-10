import json
from functools import wraps
from flask import request, jsonify
from .models import get_paginated, User
from flask_jwt_extended import get_jwt_identity


def allow_pagination(func):
    """
    Decorator for paginating results
    :param func:
    :return:
    """

    @wraps(func)
    def paginate(*args, **kwargs):
        limit = request.args.get('limit')
        page = 1 if not request.args.get('page') else request.args.get('page')

        rv = func(*args, **kwargs)[0]
        results = json.loads(rv.data)

        if limit:
            paginated = get_paginated(limit, results, request.path, page)
            if not paginated:
                return jsonify(message='The requested page was not found'), 404
            return jsonify(paginated), 200
        return func(*args, **kwargs)

    return paginate


def admin_user(func):
    """
    Decorator for protecting admin-only endpoints
    :param func:
    :return:
    """

    @wraps(func)
    def check_admin_status(*args, **kwargs):
        current_user_email = get_jwt_identity()
        user = User.get_user_by_email(current_user_email)
        if not user.is_admin:
            return jsonify(message='You are not authorized to access this resource.'), 401
        return func(*args, **kwargs)
    return check_admin_status
