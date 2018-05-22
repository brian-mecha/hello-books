import re

from flask import jsonify, request, abort, Blueprint
from jsonschema import validate
from flask_jwt_extended import create_access_token, get_raw_jwt, get_jwt_identity, jwt_required

from api.models import User, ActiveTokens, RevokedTokens
from . import user


@user.route('/api/v2/auth/register', methods=['POST'])
def register_user():
    """
    Registers a new user
    :return:
    """
    data = request.get_json()

    try:
        schema = {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
                "email": {"type": "string"},
                "is_admin": {"type": "boolean"},
            },
            "required": ["username", "password", "email"]
        }

        validate(data, schema)
    except:
        return {"Error": "Missing or wrong inputs"}, 400

    if data is None:
        return {'Message': 'No User Data Passed'}, 403

    if not data['username']:
        return {'Message': 'Username Not Provided'}, 403

    if data['username'].isspace():
        return {'Message': 'Username Not Provided'}, 403

    if not data['password']:
        return {'Message': 'Password Not Provided'}, 403

    if data['password'].isspace():
        return {'Message': 'Password Not Provided'}, 403

    valid_email = re.match(
        "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        data["email"].strip())

    if valid_email is None:
        return jsonify({'error': 'Please enter a valid Email!'}), 400

    users = User.all_users()
    users_email = [user for user in users if user.email == data["email"]]
    if users_email:
        return {"Message": "This Email already exists."}, 200

    users_username = [user for user in users if user.username == data["username"]]
    if users_username:
        return {"Message": "This Username is already taken."}, 200

    # user = User(username=data['username'], email=data['email'])
    hashed_password = User.set_password(password=data['password'])

    response = jsonify(User(username=data['username'],
                            user_password=hashed_password,
                            email=data['email'],
                            is_admin=data['is_admin']).create_user())

    return {"Message": "User registration successful."}, 201


@user.route('/api/v2/auth/login', methods=['POST'])
def login_user():
    """
    Function to login user
    :return:
    """
    user_data = request.get_json()
    # password = request.json.get('password').encode('utf-8')

    if not user_data:
        abort(401, "Login credentials missing")

    user = User.get_user_by_email(user_data["email"])

    if user is None:
        abort(401, "User does not exist")
    if not User.check_password(user_data["password"]):
        abort(200, "Wrong Username or Password")

    if not user_data["email"] or user_data["email"].isspace():
        return {"Error": "Email is missing."}, 401

    elif not user_data["password"] or user_data["password"].isspace():
        return {"Error": "Password is missing."}, 401

    access_token = create_access_token(identity=user_data["email"])

    if access_token:
        try:
            ActiveTokens(user_email=user_data["email"], access_token=access_token).create_active_token()
        except:
            return {"message": "User is already logged in."}, 200

        response = {"message": "You logged in successfully.", "token": access_token}

        return response, 200, {"access_token": access_token}
    else:
        abort(401, "Wrong User Name or Password")


@user.route('/api/v2/auth/logout', methods=['POST'])
@jwt_required
def logout_user():
    """
    Logs out the logged in user
    :return:
    """
    user_email = request.json.get('email')

    if user_email is None:
        return {"Email is required to logout"}, 403

    logged_in_user = get_jwt_identity()

    jti = get_raw_jwt()['jti']

    if logged_in_user == user_email and not RevokedTokens.is_jti_blacklisted(jti):
        revoke_token = RevokedTokens(jti=jti)
        revoke_token.revoke_token()
        ActiveTokens.find_user_with_token(user_email).delete_active_token()
        response = jsonify({'Success': 'User successfully logged out.'})

    else:
        response = jsonify(
            {'Error': 'User with email: {} is not logged in or token has been blacklisted'
                .format(user_email)})
    return response, 200


@user.route('//api/v2/auth/reset', methods=['POST'])
def user_password_reset():
    """
    Method to reset user password
    :return:
    """
    userdata = request.get_json()
    try:

        if not userdata["email"] or userdata["email"].isspace():
            return {"Error": "Email is missing."}, 401

        elif not userdata["password"] or userdata["password"].isspace():
            return {"Error": "Password is missing."}, 401

        present_user = User.get_user_by_email(userdata["email"])

        if not present_user:
            abort(401, "User with that email does not exist.")

        else:
            new_password = User.set_password(password=userdata["password"])

            # revoke = ActiveTokens(present_user).delete_active_token()

            access_token = create_access_token(identity=userdata["email"])

            if present_user.check_password(new_password):
                abort(401, "No changes detected in the password")

            present_user.user_password = new_password
            present_user.create_user()

            # ActiveTokens(user_email=userdata["email"],
            #              access_token=access_token).create_active_token()

            return {"Success": "Password reset successful."}, 200, {"jwt": access_token}

    except:
        abort(401, {"Password not Reset."})