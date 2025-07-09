from CTFd.models import db

class Zerotier(db.Model):
    __tablename__ = 'zerotier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    network_id = db.Column(db.String(128))

# Zerotier table configuration
class ZerotierConfig(db.Model):
    __tablename__ = 'zerotier_config'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='SET NULL'), nullable=True, unique=True)
    zerotier_id = db.Column(db.Integer, db.ForeignKey('zerotier.id', ondelete='SET NULL'), nullable=True)

    team = db.relationship('Teams', backref=db.backref('zerotier_config', uselist=False, lazy='joined'))
    zerotier = db.relationship('Zerotier', backref=db.backref('zerotier', uselist=False, lazy='joined'))


class JsonLogFiles(db.Model):
    __tablename__ = 'json_log_files'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id', ondelete='SET NULL'), nullable=True, unique=True)
    chall_logs = db.Column(db.JSON, nullable=True)


