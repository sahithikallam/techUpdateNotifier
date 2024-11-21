from tech.app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column('user_password', db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    last_login = db.Column(db.DateTime, nullable=True)

    # Fields for password reset functionality
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)

    # Fields for OTP functionality
    is_verified = db.Column(db.Boolean, default=False)  # Add verification status


    emailnotifications = db.Column(db.Boolean, default=False)

    subscriptions = db.relationship('Subscription', back_populates='users')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.user_password = generate_password_hash(password, salt_length=10)

    def verify_password(self, password):
        print(password)
        print(self.user_password)
        return check_password_hash(self.user_password, password)

    def to_dict(self):
        return {
            'user_id': str(self.user_id),  # Convert UUID to string
            'user_name': self.user_name,
            'user_email': self.user_email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'reset_token': self.reset_token,
            'reset_token_expiration': self.reset_token_expiration.isoformat() if self.reset_token_expiration else None,
            'emailnotifications': self.emailnotifications,
            'is_verified': self.is_verified,  # Include verification status

        }
