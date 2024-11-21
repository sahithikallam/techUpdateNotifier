from flask import request, make_response
import smtplib
import random
import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from tech.app.appMain.models.otp import OTP
from flask_restx import Resource
from tech.app.appMain import db
from tech.app.appMain.dto.otp import OtpDto
from tech.app.appMain.models import User

otp_api = OtpDto.otpapi

# Email configuration
MY_MAIL = "techupdate.notifier@gmail.com"
PASSWORD = "dgfn ytwn ihev mdxx"


@otp_api.route('/send-otp', methods=['POST'])
class SendOtp(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')

        if not email:
            return make_response({'message': 'Email is required.'}, 400)

        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))

        try:
            # Send OTP via email
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=MY_MAIL, password=PASSWORD)
                connection.sendmail(
                    from_addr=MY_MAIL,
                    to_addrs=email,
                    msg=f"Subject: OTP for Account Verification\n\n"
                        f"Your OTP for verifying your account is: {otp}\n"
                        f"Please enter this OTP to complete your verification.\n\n"
                        f"Thank you,\nTechUpdate Notifier"
                )
                print(f"OTP sent to {email}")
        except Exception as e:
            print(f"Error sending OTP: {e}")
            return make_response({'message': 'Failed to send OTP email.'}, 500)

        # Save OTP and expiry to the database
        otp_entry = OTP(email=email, otp_code=otp, expires_in_minutes=5)
        db.session.add(otp_entry)
        db.session.commit()

        return make_response({'message': 'OTP sent successfully. Please check your email.'}, 200)




@otp_api.route('/verify-otp', methods=['POST'])
class VerifyOtp(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')
        user_name = data.get('user_name')
        user_password = data.get('password')

        # Ensure required fields are provided
        if not email or not otp or not user_name or not user_password:
            return make_response({'message': 'Email, OTP, user name, and password are required.'}, 400)

        # Check if the user already exists
        existing_user = User.query.filter_by(user_email=email).first()
        if existing_user:
            return make_response({'message': 'User already exists.'}, 400)

        # Retrieve the OTP record
        otp_record = OTP.query.filter_by(email=email).order_by(OTP.created_at.desc()).first()
        if not otp_record:
            return make_response({'message': 'No OTP sent for this email.'}, 400)

        # Validate OTP and expiration
        if otp_record.otp_code == otp:
            if otp_record.expires_at > datetime.datetime.utcnow():
                # Create new user
                new_user = User(user_email=email, user_name=user_name, password=user_password, is_verified=True)
                db.session.add(new_user)
                db.session.commit()

                # Delete OTP after successful verification
                db.session.delete(otp_record)
                db.session.commit()

                return make_response({'message': 'OTP verified successfully. User is now created and verified.'}, 200)
            else:
                return make_response({'message': 'OTP has expired. Please request a new OTP.'}, 400)
        else:
            return make_response({'message': 'Invalid OTP.'}, 400)


@otp_api.route('/forgot-password/send-otp', methods=['POST'])
class ForgotPasswordSendOtp(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')

        if not email:
            return make_response({'message': 'Email is required.'}, 400)

        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))

        try:
            # Send OTP via email
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=MY_MAIL, password=PASSWORD)
                connection.sendmail(
                    from_addr=MY_MAIL,
                    to_addrs=email,
                    msg=f"Subject: OTP for Password Reset\n\n"
                        f"Your OTP for resetting your password is: {otp}\n"
                        f"Please enter this OTP to proceed with resetting your password.\n\n"
                        f"Thank you,\nTechUpdate Notifier"
                )
                print(f"OTP sent to {email}")
        except Exception as e:
            print(f"Error sending OTP: {e}")
            return make_response({'message': 'Failed to send OTP email.'}, 500)

        # Save OTP and expiry to the database
        otp_entry = OTP(email=email, otp_code=otp, expires_in_minutes=5)
        db.session.add(otp_entry)
        db.session.commit()

        return make_response({'message': 'OTP sent successfully. Please check your email.'}, 200)


@otp_api.route('/forgot-password/verify-otp', methods=['POST'])
class ForgotPasswordVerifyOtp(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')

        # Ensure required fields are provided
        if not email or not otp:
            return make_response({'message': 'Email and OTP are required.'}, 400)

        # Check if the user exists
        existing_user = User.query.filter_by(user_email=email).first()
        if not existing_user:
            return make_response({'message': 'User does not exist.'}, 404)

        # Retrieve the OTP record
        otp_record = OTP.query.filter_by(email=email).order_by(OTP.created_at.desc()).first()
        if not otp_record:
            return make_response({'message': 'No OTP sent for this email.'}, 400)

        # Validate OTP and expiration
        if otp_record.otp_code == otp:
            if otp_record.expires_at > datetime.datetime.utcnow():
                # Delete OTP after successful verification
                db.session.delete(otp_record)
                db.session.commit()

                return make_response({'message': 'OTP verified successfully. Proceed to reset your password.'}, 200)
            else:
                return make_response({'message': 'OTP has expired. Please request a new OTP.'}, 400)
        else:
            return make_response({'message': 'Invalid OTP.'}, 400)



# reset PASSWORD
@otp_api.route('/reset-password', methods=['POST'])
class ResetPassword(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        new_password = data.get('new_password')

        # Ensure required fields are provided
        if not email or not new_password:
            return make_response({'message': 'Email and new password are required.'}, 400)

        # Check if the user exists
        user = User.query.filter_by(user_email=email).first()
        if not user:
            return make_response({'message': 'User not found.'}, 404)

        # Validate that the new password is different from the current one
        if check_password_hash(user.user_password, new_password):  # Use 'user_password' field
            return make_response({'message': 'Your new password must be different from the old password.'}, 400)

        # Update the user's password
        user.user_password = generate_password_hash(new_password, salt_length=10)  # Use the correct field
        db.session.commit()

        return make_response({'message': 'Password reset successful.'}, 200)

