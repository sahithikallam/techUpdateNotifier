from tech.app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Update(db.Model):
    __tablename__ = 'updates'

    update_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tech_id = db.Column(UUID(as_uuid=True), db.ForeignKey('technology.tech_id'), nullable=False)
    update_type = db.Column(db.String(255), nullable=False)
    update_description = db.Column(db.Text, nullable=True)
    update_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    technology = db.relationship('Technology', backref='updates')

    def to_dict(self):
        return {
            'update_id': str(self.update_id),
            'tech_id': str(self.tech_id),
            'update_type': self.update_type,
            'update_description': self.update_description,
            'update_date': self.update_date.isoformat() if self.update_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

