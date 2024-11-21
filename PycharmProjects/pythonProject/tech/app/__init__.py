from flask import Blueprint
from flask_restx import Api
from tech.app.appMain.controllers.subscriptions import subscription_api
from tech.app.appMain.controllers.user import users_api
from tech.app.appMain.controllers.admins import admin_api
from tech.app.appMain.controllers.technology import technology_api
from tech.app.appMain.controllers.updates import update_api
from tech.app.appMain.controllers.otp import otp_api
from tech.app.appMain.controllers.user_notifications import usernotification_api

# Create the Blueprint
blueprint = Blueprint('api', __name__)

# Create the API object
api = Api(blueprint, title='TechUpdateNotifier')

# Add User, Admin, and Technology API namespaces
api.add_namespace(users_api, path='/user')
api.add_namespace(admin_api, path='/admin')
api.add_namespace(technology_api, path='/technology')
api.add_namespace(subscription_api, path='/subscription')
api.add_namespace(update_api, path='/update')
api.add_namespace(usernotification_api, path='/userNotification')
api.add_namespace(otp_api, path='/otp')

