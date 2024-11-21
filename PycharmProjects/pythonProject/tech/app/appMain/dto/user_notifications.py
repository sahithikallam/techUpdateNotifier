from flask_restx import Namespace, fields

class UserNotificationDto:
    usernotificationapi = Namespace('userNotifications', description='API for user notifications')