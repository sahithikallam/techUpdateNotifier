from flask_restx import Namespace

class AdminDto:
    adminapi = Namespace('admin', description='API for admin and user operations (signup, update, delete, get admin/user details)')
