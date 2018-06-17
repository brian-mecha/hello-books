from flask import jsonify

from . import errors
from api import jwt, RevokedTokens


@errors.app_errorhandler(404)
def error_404(e):
    return jsonify({"message": "The resource you are looking for " +
                               "does not exist."}), 404


@errors.app_errorhandler(400)
def error_400(e):
    return jsonify({"message": "Hello Books encountered an error while " +
                               "processing your request. Kindly try again"}), 400


@errors.app_errorhandler(401)
def error_401(e):
    return jsonify({"message": "The resource you are trying to access" +
                               " requires more privileges."}), 401


@errors.app_errorhandler(500)
def error_500(e):
    return jsonify({"message": "Hello Books was unable to process your " +
                               "request. Kindly try again"}), 500


@errors.app_errorhandler(405)
def error_500(e):
    return jsonify({"message": "The resource you are trying to access is not allowed for this requested URL."}), 500


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokens.is_jti_blacklisted(jti)


@jwt.expired_token_loader
def my_expired_token_callback():
    return jsonify({
        'msg': 'Your session has expired. Login again to continue.'
    }), 401


@jwt.revoked_token_loader
def my_expired_token_callback():
    return jsonify({
        'msg': 'Your session has expired. Login again to continue.'
    }), 401