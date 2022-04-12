from .. import db

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    userID = db.Column(db.String(100), nullable=False)
    poemaID = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User: %r %r >' % (self.id, self.score, self.comment, self.userID, self.poemaID)

    def to_json(self):
        mark_json = {
            'id': self.id,
            'score': str(self.score),
            'comment': str(self.comment),
            'userID': str(self.userID),
            'poemaID': str(self.poemaID),

        }
        return mark_json

    def to_json_short(self):
        mark_json = {
            'id': self.id,
            'score': str(self.score),
            'comment': str(self.comment),
            'userID': str(self.userID),
            'poemaID': str(self.poemaID),
        }
        return mark_json
    
    @staticmethod

    def from_json(user_json):
        id = user_json.get('id')
        score = user_json.get('score')
        comment = user_json.get('comment')
        userID = user_json.get('userID')
        poemaID = user_json.get('poemaID')

        return Mark(id=id,
                    score=score,
                    comment=comment,
                    userID=userID,
                    poemaID=poemaID
                    )