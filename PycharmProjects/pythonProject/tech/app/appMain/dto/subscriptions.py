from flask_restx import Namespace

class SubscriptionDto:
    subscription_api = Namespace('subscription', description='API for managing subscriptions ')


