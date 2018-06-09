from src import db


class BucketList(db.Model):
    """Creating the bucketlist table"""

    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """Initialize with name"""
        self.name = name

    def save(self):
        """Save new entry to db"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """delete entry from db"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all bucketlist entries"""
        return BucketList.query.all()

    def __repr__(self):
        return "BucketList {0}".format(self.name)
