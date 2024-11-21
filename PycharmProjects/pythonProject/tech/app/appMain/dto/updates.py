from flask_restx import Namespace

class UpdateDto:
    update_api = Namespace('updates', description='API for managing updates')
