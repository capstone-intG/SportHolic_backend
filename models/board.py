class Board(db.Model):
    __tablename__ = 'board'
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci' 
    }
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable=True)
    contents = db.Column(db.Text, nullable=True)
    team = db.Column(db.String(20), nullable=True)
    written_date = db.Column(db.DateTime, nullable=True)
    team = db.Column(db.String(20), nullable=True)
