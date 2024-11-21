from tech.app.appMain import db
import datetime

class OTP(db.Model):
    __tablename__ = 'otp'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, otp_code, expires_in_minutes=5):
        self.email = email
        self.otp_code = otp_code
        self.expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_in_minutes)
