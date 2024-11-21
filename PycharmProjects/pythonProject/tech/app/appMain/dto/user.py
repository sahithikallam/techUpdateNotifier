from flask_restx import Namespace

class UserDto:
    users_api = Namespace('user', description='API for user operations signup, login, update, delete, get details, reset password')
