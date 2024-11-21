import re
import secrets
from datetime import timedelta
from random import random
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request, jsonify, make_response
from flask_restx import Resource
from tech.app.appMain import db
from tech.app.appMain.models.otp import OTP
from tech.app.appMain.models.user import User
import uuid
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from tech.app.appMain.models.admins import Admins
from tech.app.appMain.dto.user import UserDto
import smtplib
from tech.app.appMain.models.user_notifications import UserNotification



users_api = UserDto.users_api

reset_token = secrets.token_urlsafe(32)  # Generates a shorter token

my_mail = "techupdate.notifier@gmail.com"
password = "dgfn ytwn ihev mdxx "

class VerifyEmail:
    def get(self, reset_token, email):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_mail, password=password)
            connection.sendmail(
                from_addr=my_mail,
                to_addrs=email,
                msg=f"Subject: Password reset request\n\n"
                    f"You requested a password reset.\n"
                    f"Click here to reset your password: http://localhost:4200/reset-password/{reset_token}\n"
                    f"If this wasn't you, please contact us at techupdate.notifier@gmail.com.\n\n"
                    f"Thank you\n"
                    f"TechUpdate Notifier"
            )
        print("Mail sent")



class VerifyMail(Resource):
    def get(self, email):
        # Generate OTP
        otp = str(random.randint(100000, 999999))

        # Send OTP via email
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_mail, password=password)
                connection.sendmail(from_addr=my_mail, to_addrs=email,
                                     msg=f"Subject: OTP for Account Verification\n\n"
                                         f"Your OTP for verifying your account is: {otp}\n"
                                         f"Please enter this OTP to complete your verification.\n\n"
                                         f"Thank you,\nTechUpdate Notifier")
            print("OTP sent successfully.")
        except Exception as e:
            print(f"Error sending email: {e}")
            return make_response({'message': 'Failed to send OTP email.'}, 500)

        # Save OTP to database for later verification
        user = User.query.filter_by(user_email=email).first()

        if user:
            user.otp = otp
            user.otp_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)  # OTP expires in 5 minutes
            db.session.commit()
            print(f"OTP {otp} saved for user {email}")
            return make_response({'message': 'OTP sent successfully. Please check your email.'}, 200)
        else:
            return make_response({'message': 'User not found.'}, 404)

class VerifyOtp(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')

        if not email or not otp:
            return make_response({'message': 'Email and OTP are required.'}, 400)

        # Find the user by email
        user = User.query.filter_by(user_email=email).first()

        if not user:
            return make_response({'message': 'User not found.'}, 404)

        # Check if the OTP matches and is within a valid time frame
        if user.otp == otp:
            otp_age = datetime.datetime.utcnow() - user.otp_expiry
            if otp_age.total_seconds() <= 0:  # OTP valid if not expired
                # OTP is valid, update user status in the DB (e.g., mark user as verified)
                user.is_verified = True
                user.otp = None  # Clear OTP after verification
                db.session.commit()
                return make_response({'message': 'OTP verified successfully. User is now verified.'}, 200)
            else:
                return make_response({'message': 'OTP has expired. Please request a new OTP.'}, 400)
        else:
            return make_response({'message': 'Invalid OTP.'}, 400)

        
# User Signup
# @users_api.route('/signup', methods=['POST'])
# class Signup(Resource):
#     def post(self):
#         data = request.get_json()
#
#         if not data.get('username') or not data.get('user_email') or not data.get('user_password'):
#             return {'message': 'Username, email, and password are required!'}, 400
#
#         existing_user_email = User.query.filter_by(user_email=data['user_email']).first()
#         if existing_user_email:
#             return {'message': 'User already exists!'}, 400
#
#         new_user = User(
#             user_id=str(uuid.uuid4()),
#             user_name=data['username'],
#             user_email=data['user_email'],
#             last_login=datetime.datetime.now()
#         )
#         new_user.password = data['user_password']
#
#         db.session.add(new_user)
#         db.session.commit()
#         return {'message': 'User created successfully!'}, 201

# User Login


@users_api.route('/signup', methods=['POST'])
class Signup(Resource):
    def post(self):
        data = request.get_json()
        print(f"Received data: {data}")  # This will log the incoming JSON

        if 'user_email' not in data or 'otp' not in data:
            print(200)
            return {'message': 'Missing user_email or otp'}, 400

        email_regex = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'

        if not re.match(email_regex, data['user_email']):

         return {'message': 'Invalid email format. Only @gmail.com is allowed.'}, 400

        # Check if the user already exists
        existing_user_email = User.query.filter_by(user_email=data['user_email']).first()

        if existing_user_email:
            return {'message': 'User already exists!'}, 400

        # Check if the email is verified
        user = User.query.filter_by(user_email=data['user_email']).first()

        if not user or not user.is_verified:
            return {'message': 'Email not verified. Please verify your email before signing up.'}, 400

        # Check if the OTP has been verified
        otp_record = OTP.query.filter_by(email=data['user_email']).order_by(OTP.created_at.desc()).first()

        if not otp_record or otp_record.expires_at < datetime.datetime.utcnow():
            return {'message': 'OTP not verified or expired. Please request a new OTP.'}, 400

        # Proceed to create a new user only if OTP is verified
        new_user = User(
            user_id=str(uuid.uuid4()),
            user_name=data['username'],
            user_email=data['user_email'],
            last_login=datetime.datetime.now(),
            is_verified=True  # Set user as verified now
        )
        new_user.password = data['user_password']  # Hash and set the password

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User successfully created and verified!'}, 201



@users_api.route('/login', methods=['POST'])
class Login(Resource):
    def post(self):
        data = request.get_json()
        password = data.get('password')

        if not data.get('email') or not data.get('password'):
            return {'message': 'Missing email or password'}, 400

        # Check if the email exists in the Admin table
        admin = Admins.query.filter_by(admin_email=data['email']).first()
        if admin and check_password_hash(admin.admin_password, data['password']):
            # Update last_login for admin
            admin.last_login = datetime.datetime.now()
            db.session.commit()  # Commit the last_login update for admin

            access_token = create_access_token(identity=admin.admin_id)
            return {
                'message': 'Admin login successful',
                'isAdmin': True,
                'token': access_token
            }, 200

        # If not found in Admin table, check in User table
        user = User.query.filter_by(user_email=data['email']).first()
        if user and  user.verify_password(password):
            # Update last_login for user
            user.last_login = datetime.datetime.now()
            db.session.commit()  # Commit the last_login
            # update for user

            access_token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1))
            return {
                'message': 'User login successful',
                'isAdmin': False,
                'token': access_token
            }, 200



        return {'message': 'Invalid credentials'}, 401

@users_api.route('/user_notifications', methods=['GET'])
class GetUserNotification(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        # Fetch notifications and order by created_at in descending order
        notifications = UserNotification.query.filter_by(user_id=user_id).order_by(UserNotification.created_at.desc()).all()

        noti_list = [notification.to_dict() for notification in notifications]

        return make_response(noti_list, 200)

# Update Last Login
# @users_api.route('/updateLastLogin', methods=['PUT'])
# class UpdateLastLogin(Resource):
#     @jwt_required()
#     def put(self):
#         data = request.get_json()
#         user_email = data.get('user_email')
#         user_password = data.get('user_password')
#
#         user = User.query.filter_by(user_email=user_email).first()
#         if user and check_password_hash(user.password, user_password):
#             user.last_login = datetime.datetime.now()  # Update last_login
#             db.session.commit()
#             return {'message': 'Last login updated successfully!'}, 200
#         else:
#             return {'message': 'Update failed!'}, 401

# Get User Details

@users_api.route('/details', methods=['GET'])
# @jwt_required()
class GetUser(Resource):
    def get(self):
        user_email = request.args.get('user_email')
        user_name = request.args.get('user_name')

        if user_email:
            user = User.query.filter_by(user_email=user_email).first()
        elif user_name:
            user = User.query.filter_by(user_name=user_name).first()
        else:
            return {'message': 'User email or username is required'}, 400

        if not user:
            return {'message': 'User not found!'}, 404

        user_data = {
            'user_id': str(user.user_id),
            'user_name': user.user_name,
            'user_email': user.user_email,
            'created_at': user.created_at,
            'last_login': user.last_login
        }
        return jsonify(user_data)

# Delete User
@users_api.route('/delete', methods=['DELETE'])
class DeleteUser(Resource):
    @jwt_required()
    def delete(self):
        user_email = request.args.get('user_email')
        user_name = request.args.get('user_name')

        if user_email:
            user = User.query.filter_by(user_email=user_email).first()
        elif user_name:
            user = User.query.filter_by(user_name=user_name).first()
        else:
            return {'message': 'User email or username is required'}, 400

        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'User not found'}, 404

# Password Reset Request
# @users_api.route('/reset-password', methods=['POST'])
# class ResetPassword(Resource):
#     def post(self):
#         data = request.get_json()
#         email = data.get('email')
#         if not email:
#             return {'message': 'Email is required'}, 400
#
#         print(f"Received email: {email}")
#
#         user = User.query.filter_by(user_email=email).first()
#         if user:
#             user_type = 'user'
#         else:
#             admin = Admins.query.filter_by(admin_email=email).first()
#             if admin:
#                 user_type = 'admin'
#             else:
#                 return {'message': 'Email not found'}, 404
#
#         reset_token = str(uuid.uuid4())
#         print(f"Generated reset token: {reset_token}")
#
#         if user:
#             user.reset_token = reset_token
#             user.reset_token_expiration = datetime.datetime.now() + datetime.timedelta(hours=2)
#             db.session.commit()
#         else:
#             admin.reset_token = reset_token
#             admin.reset_token_expiration = datetime.datetime.now() + datetime.timedelta(hours=2)
#             db.session.commit()
#
#         # Ensure VerifyMail uses the correct token and email
#         VerifyMail().get(reset_token, email)
#
#         return {'message': 'Password reset email sent'}, 200

# Reset Password with Token

@users_api.route('/reset-password', methods=['POST'])
class ResetPassword(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        if not email:
            return {'message': 'Email is required'}, 400

        print(f"Received email: {email}")

        user = User.query.filter_by(user_email=email).first()
        if user:
            target = user
        else:
            admin = Admins.query.filter_by(admin_email=email).first()
            if admin:
                target = admin
            else:
                return {'message': 'Email not found'}, 404

        try:
            # Generate secure reset token
            reset_token = secrets.token_urlsafe()
            print(f"Generated reset token: {reset_token}")

            expiration_time = datetime.datetime.now() + datetime.timedelta(hours=2)
            target.reset_token = generate_password_hash(reset_token)
            target.reset_token_expiration = expiration_time

            print("Before committing reset token...")
            db.session.commit()
            print("Reset token committed successfully.")
        except Exception as db_error:
            print(f"Database commit error: {db_error}")
            return {'message': 'Error saving reset token'}, 500

        try:
            # Send reset email
            VerifyEmail().get(reset_token, email)
            print("Reset email sent successfully.")
        except Exception as email_error:
            print(f"Email sending error: {email_error}")
            return {'message': 'Error sending reset email'}, 500

        return {'message': 'Password reset email sent'}, 200


# @users_api.route('/reset/<token>', methods=['POST'])
# class ResetWithToken(Resource):
#     def post(self, token):
#         data = request.get_json()
#         new_password = data.get('password')
#
#         if not new_password:
#             return {'message': 'New password is required'}, 400
#
#         # Check if the token belongs to a user
#         user = User.query.filter_by(reset_token=token).first()
#         if user and user.reset_token_expiration >= datetime.datetime.now():
#             user.password = generate_password_hash(new_password)
#             user.reset_token = None
#             user.reset_token_expiration = None
#             db.session.commit()
#             return {'message': 'Password has been reset successfully for user'}, 200
#
#         # Check if the token belongs to an admin
#         admin = Admins.query.filter_by(reset_token=token).first()
#         if admin and admin.reset_token_expiration >= datetime.datetime.now():
#             admin.admin_password = generate_password_hash(new_password)
#             admin.reset_token = None
#             admin.reset_token_expiration = None
#             db.session.commit()
#             return {'message': 'Password has been reset successfully for admin'}, 200
#
#         return {'message': 'Invalid or expired token'}, 400


@users_api.route('/reset/<token>', methods=['POST'])
class ResetWithToken(Resource):
    def post(self, token):
        data = request.get_json()
        new_password = data.get('password')

        if not new_password:
            return {'message': 'New password is required'}, 400

        # Search for the token
        user = User.query.filter(User.reset_token_expiration >= datetime.datetime.now()).first()
        admin = Admins.query.filter(Admins.reset_token_expiration >= datetime.datetime.now()).first()

        target = user or admin
        if target and check_password_hash(target.reset_token, token):
            target.password = generate_password_hash(new_password)
            target.reset_token = None
            target.reset_token_expiration = None
            db.session.commit()
            return {'message': 'Password has been reset successfully'}, 200

        return {'message': 'Invalid or expired token'}, 400



@users_api.route('/getUser', methods=['GET'])
class GetUser(Resource):
    @jwt_required()
    def get(self):
        # print(1)
        user_id = get_jwt_identity()
        user = User.query.filter_by(user_id=user_id).first()

        if user is None:
            return {'message': 'User not found'}, 404
        else:
            return make_response(user.to_dict(), 200)

#Edit user details
@users_api.route('/editDetails', methods=['PUT'])
class EditUser(Resource):
    def put(self):
        data = request.get_json()
        user_id = data.get('user_id')
        user_name = data.get('user_name')
        user_email = data.get('user_email')
        in_app_notifications = data.get('inappnotifications')
        email_notifications = data.get('emailnotifications')

        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        # Update user details
        user.user_name = user_name
        user.user_email = user_email
        user.inappnotifications = in_app_notifications
        user.emailnotifications = email_notifications

        try:
            db.session.commit()
            return {'message': 'User details updated successfully'}, 200
        except Exception as e:
            db.session.rollback()  # Roll back in case of an error
            return {'message': 'Error updating user data', 'error': str(e)}, 500


@users_api.route('/user/changePassword', methods=['POST'])
class ChangePassword(Resource):
    @jwt_required()  # Ensure the user is authenticated
    def post(self):
        # Get the current user from the JWT identity
        user_id = get_jwt_identity()

        # Get the password data from the request
        data = request.get_json()
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')

        if not current_password or not new_password:
            return make_response({'message': 'Both current and new passwords are required.'}, 400)

        user = User.query.get(user_id)
        if not user:
            return make_response({'message': 'User not found.'}, 404)

        # Verify the current password
        if not check_password_hash(user.password, current_password):
            return make_response({'message': 'Current password is incorrect.'}, 401)

        # Update the password
        user.password = generate_password_hash(new_password)

        try:
            db.session.commit()
            return make_response({'message': 'Password changed successfully.'}, 200)
        except Exception as e:
            db.session.rollback()
            return make_response({'message': 'Failed to update password.', 'error': str(e)}, 500)


        # Retrieve the user from the database using the user_id
        # user = User.query.filter_by(user_id=user_id).first()
        #
        # if not user:
        #     return make_response({'message': 'User not found.'}, 404)
        #
        # # Verify if the current password matches the stored password
        # if not check_password_hash(user.user_password, current_password):
        #     return make_response({'message': 'Current password is incorrect.'}, 400)
        #
        # # Hash the new password and update the user record
        # user.password = new_password  # This will automatically hash the new password
        # db.session.commit()
        #
        # return make_response({'message': 'Password changed successfully!'}, 200)









