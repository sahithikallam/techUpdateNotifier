from tech.app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash


class Admins(db.Model):
    __tablename__ = 'admins'

    admin_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(255), nullable=False)
    admin_email = db.Column(db.String(255), nullable=False, unique=True)
    admin_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    last_login = db.Column(db.TIMESTAMP)

    # Fields for password reset functionality
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        super(Admins, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.admin_password = generate_password_hash(password, salt_length=10)

    def verify_password(self, password):
        return check_password_hash(self.admin_password, password)


