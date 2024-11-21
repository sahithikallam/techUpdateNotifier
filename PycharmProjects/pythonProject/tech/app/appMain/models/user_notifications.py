from tech.app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class UserNotification(db.Model):
    __tablename__ = 'user_notifications'

    notification_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)  # Adjust based on your User model
    read = db.Column(db.Boolean, default=False)
    isactive = db.Column(db.Boolean, default=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())

    def __init__(self, **kwargs):
        super(UserNotification, self).__init__(**kwargs)

    def mark_as_read(self):
        self.read = True

    def deactivate(self):
        self.isActive = False

    def __repr__(self):
        return f'<UserNotification {self.title} for user {self.user_id}>'

    def to_dict(self):
        return {
            'notification_id': str(self.notification_id),
            'user_id': str(self.user_id),
            'read': self.read,
            'isActive': self.isactive,
            'title': self.title,
            'message': self.message,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }