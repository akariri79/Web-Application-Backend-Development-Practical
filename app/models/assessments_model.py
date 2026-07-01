from app.extensions import db

class GeneralAssessment(db.Model):
    __tablename__ = "general_assessments"
    general_assessment_id = db.Column(db.Integer, primary_key=True)
    vitals_id = db.Column(db.Integer, db.ForeignKey("vitals.vitals_id", ondelete="CASCADE"), nullable=False, unique=True)
    general_health = db.Column(db.String(20), nullable=False)
    drug_usage = db.Column(db.String(5),nullable=False)
    comments = db.Column(db.Text, nullable=False)
    vitals = db.relationship("Vitals", back_populates="general_assessment")

class OverweightAssessment(db.Model):
    __tablename__ = "overweight_assessments"
    overweight_assessment_id = db.Column(db.Integer,primary_key=True)
    vitals_id = db.Column(db.Integer, db.ForeignKey("vitals.vitals_id", ondelete="CASCADE"), nullable=False, unique=True)
    general_health = db.Column(db.String(20))
    diet_history = db.Column(db.String(5), nullable=False)
    comments = db.Column(db.Text, nullable=False)
    vitals = db.relationship("Vitals", back_populates="overweight_assessment")