from sqlalchemy.orm import backref

from tech.app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    subscription_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    tech_id = db.Column(UUID(as_uuid=True), db.ForeignKey('technology.tech_id'), nullable=False)
    subscribed_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())

    tech = db.relationship("Technology", backref='subscriptions')
    users = db.relationship("User", back_populates='subscriptions')

    def __init__(self, **kwargs):
        super(Subscription, self).__init__(**kwargs)

    def __repr__(self):
        return f"<Subscription {self.subscription_id}>"
