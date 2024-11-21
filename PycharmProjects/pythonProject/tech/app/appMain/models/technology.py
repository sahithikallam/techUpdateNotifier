from tech.app.appMain import db

class Technology(db.Model):
    __tablename__ = 'technology'

    tech_id = db.Column(db.String, primary_key=True)
    tech_name = db.Column(db.String, nullable=False)
    tech_desc = db.Column(db.String, nullable=True)
    version = db.Column(db.String, nullable=True)
    releases = db.Column(db.String, nullable=True)
    info = db.Column(db.String, nullable=True)
    tech_pic = db.Column(db.String, nullable=True)
    last_updated = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(),
                             onupdate=db.func.current_timestamp())



    def __repr__(self):
        return f"<Technology(tech_id={self.tech_id}, tech_name='{self.tech_name}', version='{self.version}', releases='{self.releases}', tech_pic='{self.tech_pic}'), info='{self.info}>"

    def to_dict(self):
        return {
            'tech_id': self.tech_id,
            'tech_name': self.tech_name,
            'tech_desc': self.tech_desc,
            'version': self.version,
            'releases': self.releases,
            'info' : self.info,
            'tech_pic': self.tech_pic,  # Include tech_pic in the dictionary representation
            'last_updated': self.last_updated
        }

