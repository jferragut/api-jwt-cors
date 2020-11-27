from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }

    def save(self):
        db.session.add(self)
        db.session.commit()