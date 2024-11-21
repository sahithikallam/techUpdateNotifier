from flask_restx import Namespace

class OtpDto:
    otpapi = Namespace('otp', description='API for managing OTPs ')


