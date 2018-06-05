import re

from flask import jsonify, request, abort
from flask_jwt_extended import create_access_token, get_raw_jwt, get_jwt_identity, jwt_required

from api.models import User, ActiveTokens, RevokedTokens, db
from . import user


@user.route('/api/v2/auth/register', methods=['POST'])
def register_user():
    """
    Registers a new user
    :return:
    """
    password = request.data.get('password')
    username = request.data.get('username')
    email = request.data.get('email')
    is_admin = request.data.get('is_admin')

    if not password or password.isspace():
        return jsonify({
            'message': 'Password Not Provided'
        }), 403

    elif not username or username.isspace():
        return jsonify({
            'message': 'Username Not Provided'
        }), 403

    elif not email or email.isspace():
        return jsonify({
            'message': 'Email Not Provided'
        }), 403

    elif is_admin is None:
        return jsonify({
            'message': 'User role not provided'
        }), 403

    if len(password) < 8:
        return {"Message": "Password should be at least 8 characters long."}, 403

    if not re.match("(^(?=[a-zA-Z0-9#@$?]{8,}$)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9]).*)", password):
        return jsonify({'message': 'Password should contain at '
                                   'least an uppercase character, lower case character and a number'}), 403

    valid_email = re.match(
        "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        email.strip())

    if valid_email is None:
        return jsonify({'error': 'Please enter a valid Email!'}), 403

    users = User.all_users()
    users_email = [user for user in users if user.email == email]
    if users_email:
        return {"Message": "This Email already exists."}, 200

    users_username = [user for user in users if user.username == username]
    if users_username:
        return {"Message": "This Username is already taken."}, 200

    hashed_password = User.set_password(password=password)

    response = jsonify(User(username=username,
                            user_password=hashed_password,
                            email=email,
                            is_admin=is_admin).create_user())

    return {"Message": "User registration successful."}, 201


@user.route('/api/v2/auth/login', methods=['POST'])
def login_user():
    """
    Function to login user
    :return:
    """
    user_data = request.get_json()

    if not user_data:
        return {"Error": "Login credentials missing"}, 401

    if user_data["email"] is None or user_data["email"].isspace():
        return {"Error": "Email is missing."}, 401

    elif not user_data["password"] or user_data["password"].isspace():
        return {"Error": "Password is missing."}, 401


    # user = User.get_user_by_email(user_data["email"])
    users = User.all_users()
    user = [user for user in users if user.email == user_data["email"]]

    if not user:
        return jsonify({'Error': 'User does not exist'}), 403
    if not User.check_password(user_data["password"]):
        return jsonify({'Error': 'Wrong Username or Password'}), 403

    access_token = create_access_token(identity=user_data["email"])

    if access_token:
        try:
            ActiveTokens(user_email=user_data["email"], access_token=access_token).create_active_token()
        except:
            return {"message": "User is already logged in."}, 200

        response = {"message": "You logged in successfully.", "access_token": access_token}

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


@user.route('/api/v2/auth/reset', methods=['POST'])
@jwt_required
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

        if len(userdata['password']) < 8:
            return {'Message': 'Password should be at least 8 characters long.'}

        present_user = User.get_user_by_email(userdata["email"])

        if not present_user:
            return {'Message': "User with that email does not exist."}, 401

        else:
            new_password = User.set_password(password=userdata["password"])

            if present_user.user_password == userdata["password"]:
                return {'Message': "No changes detected in the password"}, 401

            jti = get_raw_jwt()['jti']
            revoke_token = RevokedTokens(jti=jti)
            revoke_token.revoke_token()
            ActiveTokens.find_user_with_token(userdata["email"]).delete_active_token()
            
            present_user.user_password = new_password
            db.session.commit()

            return {"Success": "Password reset successful."}, 200

    except:
        return {"Error": "Password not Reset. Try again."}, 403
